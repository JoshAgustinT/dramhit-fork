#include <cstdint>

#include "types.hpp"
#ifdef WITH_VTUNE_LIB
#include <ittnotify.h>
#endif

#include <barrier>

#include "./hashtables/cas_kht.hpp"
#include "print_stats.h"
#include "sync.h"
#include "tests/tests.hpp"
#include "utils/hugepage_allocator.hpp"
#include "utils/vtune.hpp"
#include "zipf.h"
#include "zipf_distribution.hpp"

#ifdef ENABLE_HIGH_LEVEL_PAPI
#include <papi.h>
#endif

#ifdef WITH_PERFCPP
#include "PerfMultiCounter.hpp"
#endif

#ifdef WITH_PCM
#include "PCMCounter.hpp"
#endif

#define INFLIGHT

namespace kmercounter {
//FIX ME!
bool SINGLE_SOCKET = true;
extern void get_ht_stats(Shard *, BaseHashTable *);

extern uint64_t
    HT_TESTS_HT_SIZE;  // extern tells linker: "look for this elsewhere"
extern uint64_t HT_TESTS_NUM_INSERTS;  // remove initialization/assignment!

// default size for hashtable
// when each element is 16 bytes (2 * uint64_t), this amounts to 16 GiB
// uint64_t HT_TESTS_HT_SIZE = (1ull << 30);
// uint64_t HT_TESTS_NUM_INSERTS;
const uint64_t max_possible_threads = 128;

#ifdef WITH_PERFCPP
extern MultithreadCounter EVENTCOUNTERS;
#endif

#if defined(WITH_PCM)
extern pcm::PCMCounters pcm_cnt;
#endif
extern bool stop_sync;
extern bool zipfian_finds;
extern bool zipfian_inserts;
extern bool clear_table;

void sync_complete(void);
extern ExecPhase cur_phase;

extern std::vector<key_type, huge_page_allocator<key_type>> *g_zipf_values;

static inline uint64_t hash_knuth(uint64_t x) { return x * 2654435761u +1; }

static inline uint32_t hash_xorshift(uint32_t x) {
  x ^= x << 13;
  x ^= x >> 17;
  x ^= x << 5;
  return x;
}

OpTimings do_zipfian_inserts(
    BaseHashTable *hashtable, double skew, int64_t seed, unsigned int count,
    unsigned int id, std::barrier<std::function<void()>> *sync_barrier) {
  auto *cas_ht = static_cast<CASHashTable<KVType, ItemQueue> *>(hashtable);

  if (config.insert_factor == 0) return {1, 1};

  collector_type *const collector{};

  std::uint64_t duration{};

  sync_barrier->arrive_and_wait();
  stop_sync = true;

  InsertFindArgument *items = (InsertFindArgument *)aligned_alloc(
      64, sizeof(InsertFindArgument) * config.batch_len);

  key_type key{};
  std::size_t next_pollution{};

  uint64_t start;
  uint64_t end;
  cur_phase = ExecPhase::none;
  sync_barrier->arrive_and_wait();
  cur_phase = ExecPhase::insertions;
  if (id == 0) std::cerr << "\nSTART Insert TEST {" << std::endl;
  if (SINGLE_SOCKET) id = sched_getcpu() / 2;
  // printf("[JOSH] SIZE OF ZIPF_G[] %d, zipf_idx= %d, HT_NUM_TEST: %d\n",
  // g_zipf_values->size(), (id * HT_TESTS_NUM_INSERTS), HT_TESTS_NUM_INSERTS);
  start = RDTSC_START();

  for (auto j = 0u; j < config.insert_factor; j++) {
    // This gives all threads a place to begin fetching zipfian values from.
    // HT_TESTS_NUM_INSERTS = total_inserts/threads
    // zipfian array is HT_Size * Fill_factor
    uint64_t zipf_idx = id * HT_TESTS_NUM_INSERTS;
    uint64_t value;
    uint64_t batch_idx = 0;

    for (int i = 0; i < HT_TESTS_NUM_INSERTS; i++) {
      if (!(zipf_idx & 7) && zipf_idx + 32 < g_zipf_values->size()) {
        __builtin_prefetch(&g_zipf_values->at(zipf_idx + 32), false, 1);
      }
      value = g_zipf_values->at(zipf_idx++);
      // value = hash_knuth(zipf_idx++);
      items[batch_idx].key = items[batch_idx].value = value;
      items[batch_idx].id = i;

      if (++batch_idx == config.batch_len) {
        InsertFindArguments keypairs(items, config.batch_len);
        cas_ht->insert_batch(keypairs, collector);
        batch_idx = 0;
      }
    }
  }
  end = RDTSCP();
  duration += end - start;

  if (id == 0) std::cerr << "} END Insert TEST\n" << std::endl;

  sync_barrier->arrive_and_wait();

  return {duration, HT_TESTS_NUM_INSERTS * config.insert_factor};
}

OpTimings do_zipfian_inserts_noprefetch(
    BaseHashTable *hashtable, double skew, int64_t seed, unsigned int count,
    unsigned int id, std::barrier<std::function<void()>> *sync_barrier) {
  auto *cas_ht = static_cast<CASHashTable<KVType, ItemQueue> *>(hashtable);

  if (config.insert_factor == 0) return {1, 1};

  collector_type *const collector{};

  std::uint64_t duration{};

  sync_barrier->arrive_and_wait();
  stop_sync = true;

  InsertFindArgument *items = (InsertFindArgument *)aligned_alloc(
      64, sizeof(InsertFindArgument) * config.batch_len);

  key_type key{};
  std::size_t next_pollution{};

  uint64_t start;
  uint64_t end;
  cur_phase = ExecPhase::none;
  sync_barrier->arrive_and_wait();
  cur_phase = ExecPhase::insertions;
  if (id == 0) std::cerr << "\nSTART Insert TEST {" << std::endl;

  // printf("[JOSH] SIZE OF ZIPF_G[] %d, zipf_idx= %d, HT_NUM_TEST: %d\n",
  // g_zipf_values->size(), (id * HT_TESTS_NUM_INSERTS), HT_TESTS_NUM_INSERTS);
  start = RDTSC_START();

  for (auto j = 0u; j < config.insert_factor; j++) {
    // This gives all threads a place to begin fetching zipfian values from.
    // HT_TESTS_NUM_INSERTS = total_inserts/threads
    // zipfian array is HT_Size * Fill_factor
    uint64_t zipf_idx = id * HT_TESTS_NUM_INSERTS;
    uint64_t value;
    uint64_t batch_idx = 0;

    for (int i = 0; i < HT_TESTS_NUM_INSERTS; i++) {
      value = g_zipf_values->at(zipf_idx++);
      hashtable->insert_noprefetch(&value, collector);
    }
  }

  end = RDTSCP();
  duration += end - start;

  if (id == 0) std::cerr << "} END Insert TEST\n" << std::endl;

  sync_barrier->arrive_and_wait();

  return {duration, HT_TESTS_NUM_INSERTS * config.insert_factor};
}

OpTimings do_zipfian_gets(BaseHashTable *hashtable, unsigned int num_threads,
                          unsigned int id, auto sync_barrier) {
  auto *cas_ht = static_cast<CASHashTable<KVType, ItemQueue> *>(hashtable);

  if (config.read_factor == 0) {
    return {1, 1};
  }
  std::uint64_t duration{};
  std::uint64_t found = 0, not_found = 0;

  collector_type *const collector{};

  InsertFindArgument *items = (InsertFindArgument *)aligned_alloc(
      64, sizeof(InsertFindArgument) * config.batch_len);

  FindResult *results = new FindResult[config.batch_len];

  ValuePairs vp = std::make_pair(0, results);
  sync_barrier->arrive_and_wait();  // this calls sync_complete
  stop_sync = true;

  // THis ensures that for a given hashtable size, regardless of
  // the fill factor, number of finds is the same.
  // const uint64_t num_finds = config.ht_size / num_threads;
  const uint64_t num_finds = HT_TESTS_NUM_INSERTS;  // old zipf test

  uint64_t start;
  uint64_t end;

  std::uint64_t key{};
  std::size_t next_pollution{};

  // char *vtune_evt_name = (char *)malloc(16);
  // __itt_event vtune_evt;
  if (id == 0) std::cerr << "\nSTART FIND TEST {" << std::endl;

  if (SINGLE_SOCKET) id = sched_getcpu() / 2;

  start = RDTSC_START();

  for (auto j = 0u; j < config.read_factor; j++) {
    // This gives all threads a place to begin fetching zipfian values from.
    // HT_TESTS_NUM_INSERTS = total_inserts/threads
    // zipfian array is HT_Size * Fill_factor
    uint64_t zipf_idx = id * HT_TESTS_NUM_INSERTS;
    uint64_t value;
    uint64_t batch_idx = 0;

    for (int i = 0; i < HT_TESTS_NUM_INSERTS; i++) {
      if (!(zipf_idx & 7) && zipf_idx + 32 < g_zipf_values->size()) {
        __builtin_prefetch(&g_zipf_values->at(zipf_idx + 32), false, 1);
      }
      value = g_zipf_values->at(zipf_idx++);
      // value = hash_knuth(zipf_idx++);
      items[batch_idx].key = items[batch_idx].value = value;
      items[batch_idx].id = i;

      if (++batch_idx == config.batch_len) {
        vp.first = 0;
        cas_ht->find_batch(InsertFindArguments(items, config.batch_len), vp,
                           collector);
        found += vp.first;
        vp.first = 0;
        batch_idx = 0;
      }
    }
  }

  end = RDTSCP();
  duration += end - start;

  if (id == 0) std::cerr << "} END FIND TEST\n" << std::endl;
  sync_barrier->arrive_and_wait();

  if (found > 0) {
    PLOGI.printf("DEBUG: thread %u | actual found %lu | cycles per get: %lu",
                 id, found, duration / found);
  }

  // We need to count the cachelines from our zipfian prefetch, our local zipf
  // set is HT_TESTS_NUM_INSERTS of keys we prefetch every 8, since 8 fit in
  // cacheline, so we should count additional HT_TESTS_NUM_INSERTS/8
  // return {duration, (HT_TESTS_NUM_INSERTS+(HT_TESTS_NUM_INSERTS/8)) *
  // config.read_factor};
  return {duration, HT_TESTS_NUM_INSERTS * config.read_factor};
  return {duration, found};
}

OpTimings do_zipfian_gets_noprefetch(BaseHashTable *hashtable,
                                     unsigned int num_threads, unsigned int id,
                                     auto sync_barrier) {
  auto *cas_ht = static_cast<CASHashTable<KVType, ItemQueue> *>(hashtable);

  if (config.read_factor == 0) {
    return {1, 1};
  }
  std::uint64_t duration{};
  std::uint64_t found = 0, not_found = 0;

  collector_type *const collector{};

  InsertFindArgument *items = (InsertFindArgument *)aligned_alloc(
      64, sizeof(InsertFindArgument) * config.batch_len);

  FindResult *results = new FindResult[config.batch_len];

  ValuePairs vp = std::make_pair(0, results);
  sync_barrier->arrive_and_wait();  // this calls sync_complete
  stop_sync = true;

  // THis ensures that for a given hashtable size, regardless of
  // the fill factor, number of finds is the same.
  // const uint64_t num_finds = config.ht_size / num_threads;
  const uint64_t num_finds = HT_TESTS_NUM_INSERTS;  // old zipf test

  uint64_t start;
  uint64_t end;

  std::uint64_t key{};
  std::size_t next_pollution{};

  // char *vtune_evt_name = (char *)malloc(16);
  // __itt_event vtune_evt;
  if (id == 0) std::cerr << "\nSTART FIND TEST {" << std::endl;

  start = RDTSC_START();

  for (auto j = 0u; j < config.read_factor; j++) {
    // This gives all threads a place to begin fetching zipfian values from.
    // HT_TESTS_NUM_INSERTS = total_inserts/threads
    // zipfian array is HT_Size * Fill_factor
    uint64_t zipf_idx = id * HT_TESTS_NUM_INSERTS;
    uint64_t value;
    uint64_t batch_idx = 0;

    for (int i = 0; i < HT_TESTS_NUM_INSERTS; i++) {
      value = g_zipf_values->at(zipf_idx++);
      bool ret = hashtable->find_noprefetch(&value, collector);
      if (ret) found++;
    }
  }

  end = RDTSCP();
  duration += end - start;

  if (id == 0) std::cerr << "} END FIND TEST\n" << std::endl;
  sync_barrier->arrive_and_wait();

  if (found > 0) {
    PLOGI.printf("DEBUG: thread %u | actual found %lu | cycles per get: %lu",
                 id, found, duration / found);
  }

  // We need to count the cachelines from our zipfian prefetch, our local zipf
  // set is HT_TESTS_NUM_INSERTS of keys we prefetch every 8, since 8 fit in
  // cacheline, so we should count additional HT_TESTS_NUM_INSERTS/8
  // return {duration, (HT_TESTS_NUM_INSERTS+(HT_TESTS_NUM_INSERTS/8)) *
  // config.read_factor};
  return {duration, HT_TESTS_NUM_INSERTS * config.read_factor};
  return {duration, found};
}

void ZipfianTest::run(Shard *shard, BaseHashTable *hashtable, double skew,
                      int64_t zipf_seed, unsigned int count,
                      std::barrier<std::function<void()>> *sync_barrier) {
  OpTimings insert_timings{};
  OpTimings find_timings{};
  OpTimings upsertion_timings{1, 1};

  CASHashTable<KVType, ItemQueue> *cas_ht =
      static_cast<CASHashTable<KVType, ItemQueue> *>(hashtable);

  // generate zipfian here.
  std::vector<key_type, huge_page_allocator<key_type>> *zipf_set_local;

  cur_phase = ExecPhase::insertions;

  PLOGV.printf(
      "Zipfian test run: thread %u, ht size: %lu, insertions: %lu, skew "
      "%f",
      shard->shard_idx, config.ht_size, HT_TESTS_NUM_INSERTS, skew);

  if (config.no_prefetch) {
    insert_timings = do_zipfian_inserts_noprefetch(
        hashtable, skew, zipf_seed, count, shard->shard_idx, sync_barrier);
  } else {
    insert_timings = do_zipfian_inserts(hashtable, skew, zipf_seed, count,
                                        shard->shard_idx, sync_barrier);
  }

  shard->stats->insertions = insert_timings;

  cur_phase = ExecPhase::finds;

  if (config.no_prefetch) {
    find_timings = do_zipfian_gets_noprefetch(hashtable, count,
                                              shard->shard_idx, sync_barrier);
  } else {
    find_timings =
        do_zipfian_gets(hashtable, count, shard->shard_idx, sync_barrier);
  }

  shard->stats->finds = find_timings;
  shard->stats->ht_fill = config.ht_fill;
  get_ht_stats(shard, hashtable);

  sync_barrier->arrive_and_wait();

  if (shard->shard_idx == 0) {
    PLOGI.printf("get fill %.3f",
                 (double)cas_ht->get_fill() / cas_ht->get_capacity());
  }
}

}  // namespace kmercounter
