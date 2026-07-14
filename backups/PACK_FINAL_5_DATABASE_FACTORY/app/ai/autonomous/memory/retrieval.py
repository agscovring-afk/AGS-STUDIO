class MemoryRetriever:


    def search(self, records, keyword):

        results = []

        for item in records:

            text = str(item).lower()

            if keyword.lower() in text:
                results.append(item)


        return results



retriever = MemoryRetriever()