from __future__ import annotations
from functools import cmp_to_key

from InformationRetrieval.Document.AbstractCollection import AbstractCollection
from InformationRetrieval.Document.DocumentType import DocumentType
from InformationRetrieval.Document.IndexType import IndexType
from InformationRetrieval.Document.Parameter import Parameter
from InformationRetrieval.Index.CategoryNode import CategoryNode
from InformationRetrieval.Index.CategoryTree import CategoryTree
from InformationRetrieval.Index.IncidenceMatrix import IncidenceMatrix
from InformationRetrieval.Index.InvertedIndex import InvertedIndex
from InformationRetrieval.Index.NGramIndex import NGramIndex
from InformationRetrieval.Index.PositionalIndex import PositionalIndex
from InformationRetrieval.Index.TermDictionary import TermDictionary
from InformationRetrieval.Index.TermOccurrence import TermOccurrence
from InformationRetrieval.Index.TermType import TermType
from InformationRetrieval.Query.FocusType import FocusType
from InformationRetrieval.Query.Query import Query
from InformationRetrieval.Query.QueryResult import QueryResult
from InformationRetrieval.Query.RetrievalType import RetrievalType
from InformationRetrieval.Query.SearchParameter import SearchParameter


class MemoryCollection(AbstractCollection):

    __index_type: IndexType

    def __init__(self,
                 directory: str,
                 parameter: Parameter):
        super().__init__(directory, parameter)
        self.__index_type = parameter.getIndexType()
        if parameter.loadIndexesFromFile():
            self.loadIndexesFromFile(directory)
        else:
            self.constructIndexesInMemory()
        if parameter.getDocumentType() == DocumentType.CATEGORICAL:
            self.positional_index.setCategoryCounts(self.documents)
            self.category_tree.setRepresentativeCount(parameter.getRepresentativeCount())

    def loadIndexesFromFile(self, directory: str):
        self.dictionary = TermDictionary(self.comparator, directory)
        self.inverted_index = InvertedIndex(directory)
        if self.parameter.constructPositionalIndex():
            self.positional_index = PositionalIndex(directory)
            self.positional_index.setDocumentSizes(self.documents)
        if self.parameter.constructPhraseIndex():
            self.phrase_dictionary = TermDictionary(self.comparator, directory + "-phrase")
            self.phrase_index = InvertedIndex(directory + "-phrase")
            if self.parameter.constructPositionalIndex():
                self.phrase_positional_index = PositionalIndex(directory + "-phrase")
        if self.parameter.constructNGramIndex():
            self.bi_gram_dictionary = TermDictionary(self.comparator, directory + "-biGram")
            self.tri_gram_dictionary = TermDictionary(self.comparator, directory + "-triGram")
            self.bi_gram_index = NGramIndex(directory + "-biGram")
            self.tri_gram_index = NGramIndex(directory + "-triGram")

    def save(self):
        if self.__index_type == IndexType.INVERTED_INDEX:
            self.dictionary.save(self.name)
            self.inverted_index.save(self.name)
            if self.parameter.constructPositionalIndex():
                self.positional_index.save(self.name)
            if self.parameter.constructPhraseIndex():
                self.phrase_dictionary.save(self.name + "-phrase")
                self.phrase_index.save(self.name + "-phrase")
                if self.parameter.constructPositionalIndex():
                    self.phrase_positional_index.save(self.name + "-phrase")
            if self.parameter.constructNGramIndex():
                self.bi_gram_dictionary.save(self.name + "-biGram")
                self.tri_gram_dictionary.save(self.name + "-triGram")
                self.bi_gram_index.save(self.name + "-biGram")
                self.tri_gram_index.save(self.name + "-triGram")
        if self.parameter.getDocumentType() == DocumentType.CATEGORICAL:
            self.saveCategories()

    def saveCategories(self):
        output_file = open(self.name + "-categories.txt", mode="w", encoding="utf-8")
        for document in self.documents:
            output_file.write(document.getDocId().__str__() + "\t" + document.getCategory().__str__() + "\n")
        output_file.close()

    def constructIndexesInMemory(self):
        terms = self.constructTerms(TermType.TOKEN)
        self.dictionary = TermDictionary(self.comparator, terms)
        if self.__index_type == IndexType.INCIDENCE_MATRIX:
            self.incidence_matrix = IncidenceMatrix(terms, self.dictionary, len(self.documents))
        elif self.__index_type == IndexType.INVERTED_INDEX:
            self.inverted_index = InvertedIndex(self.dictionary, terms)
            if self.parameter.constructPositionalIndex():
                self.positional_index = PositionalIndex(self.dictionary, terms)
            if self.parameter.constructPhraseIndex():
                terms = self.constructTerms(TermType.PHRASE)
                self.phrase_dictionary = TermDictionary(self.comparator, terms)
                self.phrase_index = InvertedIndex(self.phrase_dictionary, terms)
                if self.parameter.constructPositionalIndex():
                    self.phrase_positional_index = PositionalIndex(self.phrase_dictionary, terms)
            if self.parameter.constructNGramIndex():
                self.constructNGramIndex()
            if self.parameter.getDocumentType() == DocumentType.CATEGORICAL:
                self.category_tree = CategoryTree(self.name)
                for document in self.documents:
                    document.loadCategory(self.category_tree)

    def constructTerms(self, termType: TermType) -> [TermOccurrence]:
        terms: [TermOccurrence] = []
        for doc in self.documents:
            document_text = doc.loadDocument()
            doc_terms = document_text.constructTermList(doc.getDocId(), termType)
            terms.extend(doc_terms)
        terms.sort(key=cmp_to_key(TermOccurrence.termOccurrenceComparator))
        return terms

    def attributeSearch(self, query: Query, parameter: SearchParameter) -> QueryResult:
        term_attributes = Query()
        phrase_attributes = Query()
        term_result = QueryResult()
        phrase_result = QueryResult()
        filtered_query = query.filterAttributes(self.attribute_list, term_attributes, phrase_attributes)
        if term_attributes.size() > 0:
            term_result = self.inverted_index.search(term_attributes, self.dictionary)
        if phrase_attributes.size() > 0:
            phrase_result = self.phrase_index.search(phrase_attributes, self.phrase_dictionary)
        if term_attributes.size() == 0:
            attribute_result = phrase_result
        elif phrase_attributes.size() == 0:
            attribute_result = term_result
        else:
            attribute_result = term_result.intersectionFastSearch(phrase_result)
        if filtered_query.size() == 0:
            return attribute_result
        else:
            filtered_result = self.searchWithInvertedIndex(filtered_query, parameter)
            if parameter.getRetrievalType() != RetrievalType.RANKED:
                return filtered_result.intersectionFastSearch(attribute_result)
            elif attribute_result.size() < 10:
                return filtered_result.intersectionLinearSearch(attribute_result)
            else:
                return filtered_result.intersectionBinarySearch(attribute_result)

    def searchWithInvertedIndex(self,
                                query: Query,
                                searchParameter: SearchParameter) -> QueryResult:
        if searchParameter.getRetrievalType() == RetrievalType.BOOLEAN:
            return self.inverted_index.search(query, self.dictionary)
        elif searchParameter.getRetrievalType() == RetrievalType.POSITIONAL:
            return self.positional_index.positionalSearch(query, self.dictionary)
        elif searchParameter.getRetrievalType() == RetrievalType.RANKED:
            return self.positional_index.rankedSearch(query,
                                                        self.dictionary,
                                                        self.documents,
                                                        searchParameter.getTermWeighting(),
                                                        searchParameter.getDocumentWeighting(),
                                                        searchParameter.getDocumentsRetrieved())
        else:
            return QueryResult()

    def filterAccordingToCategories(self,
                                    currentResult: QueryResult,
                                    categories: [CategoryNode]):
        filtered_result = QueryResult()
        items = currentResult.getItems()
        for query_result_item in items:
            category_node = self.documents[query_result_item.getDocId()].getCategoryNode()
            for possible_ancestor in categories:
                if category_node.isDescendant(possible_ancestor):
                    filtered_result.add(query_result_item.getDocId(), query_result_item.getScore())
                    break
        return filtered_result

    def autoCompleteWord(self, prefix: str) -> [str]:
        result = []
        i = self.dictionary.getWordStartingWith(prefix)
        while i < self.dictionary.size():
            if self.dictionary.getWordWithIndex(i).getName().startswith(prefix):
                result.append(self.dictionary.getWordWithIndex(i).getName())
            else:
                break
            i = i + 1
        self.inverted_index.autoCompleteWord(result, self.dictionary)
        return result

    def searchCollection(self,
                         query: Query,
                         searchParameter: SearchParameter):
        if searchParameter.getFocusType() == FocusType.CATEGORY:
            if searchParameter.getSearchAttributes():
                current_result = self.attributeSearch(query, searchParameter)
            else:
                current_result = self.searchWithInvertedIndex(query, searchParameter)
            categories = self.category_tree.getCategories(query,
                                                            self.dictionary,
                                                            searchParameter.getCategoryDeterminationType())
            return self.filterAccordingToCategories(current_result, categories)
        else:
            if self.__index_type == IndexType.INCIDENCE_MATRIX:
                return self.incidence_matrix.search(query, self.dictionary)
            elif self.__index_type == IndexType.INVERTED_INDEX:
                if searchParameter.getSearchAttributes():
                    return self.attributeSearch(query, searchParameter)
                else:
                    return self.searchWithInvertedIndex(query, searchParameter)
            else:
                return QueryResult()
