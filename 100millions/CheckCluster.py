from tqdm import tqdm
from datasketch import MinHash, MinHashLSH


def main() -> None:
    for _ in tqdm(range(1), desc="Create finding example:"):
        hash = [
            45257595, 32446431, 15996061, 8009856, 14517282, 21932930, 12845057,
            37042528, 7236594, 7822468, 27440202, 28724811, 9871730, 20216309,
            16722991, 2495725, 7639270, 10370260, 46268854, 13272941, 8935264,
            6992914, 3272670, 10928280, 6508211, 16654569, 3283936, 26406731,
            3623948, 22077072, 19831117, 22512651, 14239205, 620249, 25843007,
            37772565, 4984953, 2014910, 41112238, 29448427, 1301305, 20997145,
            3568057, 25498399, 19008744, 20401045, 12670983, 9616699, 22681408,
            55893991, 23726708, 63517729, 17533389, 4219880, 26902933, 18468540,
            111682768, 3920875, 7981408, 6437796, 15652450, 3280917, 50528181,
            17994371, 7008185, 15672725, 13186711, 13154950, 3877062, 4674130,
            9968447, 21294843, 11529635, 2621713, 10107236, 8152315, 34198592,
            5893758, 7208336, 3327722, 22265064, 33559997, 25892418, 4809431,
            16649562, 28924652, 5918964, 17780158, 8775282, 22114145, 5644413,
            64601861, 6649022, 14312031, 505398, 60496599, 26794549, 6412726,
            31331500, 5865279, 1561486, 2325275, 27368131, 55474058, 14789730,
            2618114, 9349325, 59058051, 23410937, 33766879, 5050437, 11613306,
            16615654, 16013747, 19421495, 34650392, 3544689, 911917, 31528895,
            22331528, 33150355, 21074917, 12554342, 11341101, 34488618, 59766859,
            4704630, 16403646, 45846798, 48937414, 34515335, 12327745, 56655840,
            67898377, 11847291, 10440127, 52206854, 1472071, 50877405, 2608031,
            23757896, 1317127, 3729161, 3008327, 8269650, 24382696, 22259772,
            13341219, 41635571, 45720643, 55436514, 11314584, 14112712, 20719054,
            6029495, 6066917, 17617319, 20912683, 487658, 12694918, 16736949,
            2050554, 929254, 2439935, 23402018, 25942551, 14997677, 30168864,
            11725003, 27377607, 58336899, 32945145, 3669809, 6774546, 47019845,
            21124247, 3729516, 50346019, 5205345, 17956138, 74772136, 14186475,
            9872481, 9819306, 21526394, 36145227, 28190939, 78404653, 11999632,
            5636280, 711013, 22449649, 17750167, 135411, 31737332, 19435526,
            17828669, 14778501, 25907974, 64473656, 3537610, 10224550, 11104581,
            3581119, 10125714, 4872325, 23275123, 20921234, 25316042, 47656243,
            5495247, 55427667, 5926344, 13589829, 26042628, 3974143, 29452951,
            24198655, 994382, 28852957, 2869995, 14225512, 9384980, 4202318,
            461562, 23104064, 1975250, 33208325, 46171316, 336324, 46585084,
            8809453, 17522213, 9160233, 39609450, 6060385, 1773449, 20728692,
            50304185, 60411203, 45151628, 37564996, 44090014, 3361287, 2321950,
            57227376, 8639756, 24659425, 52493256, 10348166, 9626648, 12546638,
            7125338, 35879063, 7349702, 30142478
        ]
        minhash = MinHash(num_perm=256, hashvalues=hash)

    for _ in tqdm(range(1), desc="Connect to existing db:"):
        lsh = MinHashLSH(
            threshold=0.5, num_perm=256, storage_config={
                'type': 'cassandra',
                'basename': b'perftest',
                'cassandra': {
                    'seeds': ['127.0.0.1'],
                    'keyspace': 'th_millions_perfomance',
                    'replication': {
                        'class': 'SimpleStrategy',
                        'replication_factor': '1',
                    },
                    'drop_keyspace': False,
                    'drop_tables': False,
                }
            }
        )

    try:
        for _ in tqdm(range(1), desc="Find minHash similarity:"):
            result = lsh.query(minhash)
        print("Approximate neighbours with Jaccard similarity > 0.5", len(result))
    except BaseException as e:
        print(str(e))
        print("Error")


if __name__ == "__main__":
    main()
