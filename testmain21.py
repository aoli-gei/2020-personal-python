import GHAnalysis
import unittest

class manitest(unittest.TestCase):
    
    def test_init(self):
        x=GHAnalysis.Data("test",1)
    
    def test_find(self):
        x=GHAnalysis.Data("test",1)
        x.getEventsUsers("whq","PushEvent")
        x.getEventsRepos("jkl","PushEvent")
        x.getEventsUsersAndRepos("jkl","fds","PushEvent")
    '''
    def test_run(self):
        x=GHAnalysis.Run()

    #def test_find2(self):
    '''

if __name__ == '__main__':
    unittest.main(verbosity=2)