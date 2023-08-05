from InformationRetrieval.Index.TermDictionary cimport TermDictionary
from InformationRetrieval.Query.Query cimport Query
from InformationRetrieval.Query.QueryResult cimport QueryResult

cdef class PositionalIndex:

    cdef object __positional_index

    cpdef readPositionalPostingList(self, str fileName)
    cpdef saveSorted(self, str fileName)
    cpdef save(self, str fileName)
    cpdef addPosition(self, int termId, int docId, int position)
    cpdef QueryResult positionalSearch(self, Query query, TermDictionary dictionary)
    cpdef list getTermFrequencies(self, int docId)
    cpdef list getDocumentFrequencies(self)
    cpdef setDocumentSizes(self, list documents)
    cpdef setCategoryCounts(self, list documents)
    cpdef QueryResult rankedSearch(self,
                     Query query,
                     TermDictionary dictionary,
                     list documents,
                     object termWeighting,
                     object documentWeighting,
                     documentsReturned: int)
