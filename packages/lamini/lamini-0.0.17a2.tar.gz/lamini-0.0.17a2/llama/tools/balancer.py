from random import Random
from llama.program.util.run_ai import query_run_embedding
from llama.program.util.run_ai import fuzzy_is_duplicate


class DatasetBalancer:
    """Balance your dataset with embeddings"""

    removed_indices = []
    removed_data = []
    new_dataset = []
    new_indices = []
    balanced_index = []
    index = []

    def get_all_embeddings(self, dataset):
        self.index = []
        for i in range(0, len(dataset), 32):
            # Get embeddings
            print("Processing Embeddings: " + str(i) + " of " + str(len(dataset)))
            embeddings = query_run_embedding(dataset[i : i + 32])
            self.index.extend(embeddings)

        return self.index

    def stochastic_balance_dataset(self, dataset, sample_size=1, threshold=0.99):
        self.balanced_index = []
        self.new_indices = []
        self.new_dataset = []
        index = self.get_all_embeddings(dataset)
        rand = Random()
        for i in range(len(dataset)):
            print("Comparing: " + str(i) + " of " + str(len(dataset)))
            # print("Balanced Index: " + str(len(balanced_index)))
            # Get embeddings
            embedding = index[i]
            random_sample = rand.sample(
                self.balanced_index, min(sample_size, len(self.balanced_index))
            )
            if not fuzzy_is_duplicate(embedding, random_sample, threshold):
                print("Adding: " + str(i) + " of " + str(len(dataset)))
                self.balanced_index.append(embedding)
                self.new_indices.append(i)
                self.new_dataset.append(dataset[i])
            else:
                self.removed_indices.append(i)
                self.removed_data.append(dataset[i])

        return self.new_dataset

    def full_balance_dataset(self, dataset, threshold=0.99):
        self.balanced_index = []
        self.new_indices = []
        self.new_dataset = []
        index = self.get_all_embeddings(dataset)
        for i in range(len(dataset)):
            print("Processing: " + str(i) + " of " + str(len(dataset)))
            # print("Balanced Index: " + str(len(balanced_index)))
            # Get embeddings
            embedding = index[i]
            if not fuzzy_is_duplicate(embedding, self.balanced_index, threshold):
                print("Adding: " + str(i) + " of " + str(len(dataset)))
                self.balanced_index.append(embedding)
                self.new_indices.append(i)
                self.new_dataset.append(dataset[i])
            else:
                self.removed_indices.append(i)
                self.removed_data.append(dataset[i])

        return self.new_dataset
