from math import sqrt

from InformationRetrieval.Index.PostingSkip cimport PostingSkip

cdef class PostingSkipList(PostingList):

    def __init__(self):
        super().__init__()
        self.__skipped = False

    cpdef add(self, int docId):
        cdef PostingSkip p
        cdef PostingSkip last
        p = PostingSkip(docId)
        last = self.__postings[len(self.__postings) - 1]
        last.setNext(p)
        self.__postings.append(p)

    cpdef addSkipPointers(self):
        cdef int N, i, j, posting, skip
        cdef PostingSkip current
        N = int(sqrt(self.size()))
        if not self.__skipped:
            self.__skipped = True
            i = 0
            posting = 0
            while posting != len(self.__postings):
                if i % N == 0 and i + N < self.size():
                    j = 0
                    skip = posting
                    while j < N:
                        j = j + 1
                        skip = skip + 1
                    current = self.__postings[posting]
                    current.addSkip(self.__postings[skip])
                posting = posting + 1
                i = i + 1

    cpdef PostingList intersection(self, PostingList secondList):
        cdef PostingSkip p1, p2
        p1 = self.__postings[0]
        p2 = secondList.__postings[0]
        result = PostingSkipList()
        while p1 is not None and p2 is not None:
            if p1.getId() == p2.getId():
                result.add(p1.getId())
                p1 = p1.next()
                p2 = p2.next()
            else:
                if p1.getId() < p2.getId():
                    if self.__skipped and p1.hasSkip() and p1.getSkip().getId() < p2.getId():
                        while p1.hasSkip() and p1.getSkip().getId() < p2.getId():
                            p1 = p1.getSkip()
                    else:
                        p1 = p1.next()
                else:
                    if self.__skipped and p2.hasSkip() and p2.getSkip().getId() < p1.getId():
                        while p2.hasSkip() and p2.getSkip().getId() < p1.getId():
                            p2 = p2.getSkip()
                    else:
                        p2 = p2.next()
        return result
