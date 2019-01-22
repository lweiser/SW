#!/usr/bin/env python
import boardspace, sw_exceptions
import unittest
class TestSpaceInit_Basics(unittest.TestCase):
    def setUp(self):
        self.space = boardspace.BoardSpace(1,'farm')

    def test_terrain(self):
        '''Check terrain setting'''
        self.assertEqual(self.space.terrain,'farm')

    def test_owner_is_none(self):
        '''Check that space is initialized to none'''
        self.assertIsNone(self.space.owner)

    def test_symbol_is_none(self):
        '''Check that symbol is initialized to none'''
        self.assertIsNone(self.space.symbol)


class TestSpaceInit_Restrictions(unittest.TestCase):
    """Class for testing initialization restrictions for space"""

    def test_terrain_input_asserition(self):
        '''Tests that errors are thrown for wrong terrain input'''
        for t in ['Farm','abbey','swamps']:
            # with is used here because
            # this sets up and tares down the class every time.
            with self.assertRaises(sw_exceptions.InputError):
                boardspace.BoardSpace(1,t,False,False,None)

    def test_symbol_restriction_on_swamps(self):
        '''Tests that an exception is raised for symbol spelling errors'''
        for s in ['MagicSource','lost_tribes','swamps']:
            # with is used here because
            # this sets up and tares down the class every time.
            with self.assertRaises(sw_exceptions.InputError):
                boardspace.BoardSpace(1,'swamps',False,False,s)

    def test_no_lost_tribes_on_mountain(self):
        '''Tests that exception is raised for lost_tribes placed on mountain '''
        with self.assertRaises(sw_exceptions.InputError):
            boardspace.BoardSpace(1,'mountain',False,True,None)

    def test_lost_tribes_exception_None(self):
        '''Tests that lost_tribes throws an error when set to None '''
        with self.assertRaises(TypeError):
            boardspace.BoardSpace(1,'swamp',False,None,None)

    def test_lost_tribes_exception_one(self):
        '''Tests that lost_tribes throws an error when set to an int '''
        with self.assertRaises(TypeError):
            boardspace.BoardSpace(1,'swamp',False,1,None)

    def test_lost_tribes_exception_zero(self):
        '''Tests that lost_tribes throws an error when set to an int '''
        with self.assertRaises(TypeError):
            boardspace.BoardSpace(1,'swamp',False,0,None)

    def test_lost_tribes_exception_string(self):
        '''Tests that lost_tribes throws an error when set to a string'''
        with self.assertRaises(TypeError):
            boardspace.BoardSpace(1,'swamp',False,'lost_tribes',None)

    def test_no_zero_id(self):
        '''Tests that exception is raised for space_id set to 0'''
        with self.assertRaises(sw_exceptions.InputError):
            boardspace.BoardSpace(0,'swamp',False)

    def test_no_negative_id(self):
        '''Tests that exception is raised for negative space ids'''
        with self.assertRaises(sw_exceptions.InputError):
            boardspace.BoardSpace(-1,'swamp',False)

    def test_no_string_id(self):
        '''Tests that string ids raise an exception'''
        with self.assertRaises(TypeError):
            boardspace.BoardSpace('a','swamp')

    def test_no_float_id(self):
        '''Tests that float ids raise an exception'''
        with self.assertRaises(TypeError):
            boardspace.BoardSpace(1.4,'swamp')


# this code for error handling was found at https://docs.python.org/2/tutorial/errors.html

class TestSpaceInit_LostTribes(unittest.TestCase):
    """Tests space initialization for lost tribes"""

    def setUp(self):
        self.space = boardspace.BoardSpace(1,'swamp',False,True,None)

    def test_lost_tribes_sets_owner(self):
        '''Tests that lost_tribes option adds properly'''
        self.assertEqual(self.space.owner,'lost_tribes')

    def token_count_lost_tribes(self):
        '''Tests that 2 'lost_tribes' tokens are added '''
        self.assertEqual(self.space.tokens['lost_tribes']==2)

class TestSpaceInit_Mountain(unittest.TestCase):
    ''' Tests initialization cases specific to mountain spaces '''

    def setUp(self):
        self.space = boardspace.BoardSpace(1,'mountain')

    def test_terrain_name(self):
        '''tests that space.terrain is set to 'mountain'''
        self.assertEqual(self.space.terrain,'mountain')

    def test_token_dict_membership(self):
        '''tests that the 'mountain' value is added to the tokens dict'''
        self.assertIn('mountain', self.space.tokens)

    def test_token_count(self):
        '''Tests that setup assigns 1 mountain token'''
        self.assertEqual(self.space.tokens['mountain'],1)

class TestEdgeInit_Edges(unittest.TestCase):
    ''' Tests initialization cases specific to edge spaces '''

    def test_edge_None(self):
        '''Test that edge variable not assigned to None'''
        with self.assertRaises(TypeError):
            boardspace.BoardSpace('a','swamp',None)

    def test_edge_string(self):
        '''Test that edge varible not assigned a string'''
        with self.assertRaises(TypeError):
            boardspace.BoardSpace('a','swamp','edge')

    def test_edge_float(self):
        '''Test that edge varible not assigned a float'''
        with self.assertRaises(TypeError):
            boardspace.BoardSpace('a','swamp',1)

class TestSpaceFunctions(unittest.TestCase):
    '''Tests a few of the smaller space functions'''
    def setUp(self):
        # i'll initialize this one with a different set of test cases
        self.space = boardspace.BoardSpace(1, 'farm')

    # tests for the add_tokens function
    def test_add_tokens_negative_value(self):
        '''Tests if assigning negative token values leads to error'''
        with self.assertRaises(sw_exceptions.InputError):
            self.space.add_tokens('generic_tokens',-5)

    def test_add_tokens_zero_values(self):
        '''Tests if assigning 0 tokens leads to error'''
        with self.assertRaises(sw_exceptions.InputError):
            self.space.add_tokens('generic_tokens',0)

    def test_add_tokens_non_int(self):
        '''Tests if assigning a string to add tokens leads to error'''
        with self.assertRaises(TypeError):
            self.space.add_tokens('generic_tokens','tokens')

    def test_add_tokens_token_number(self):
        self.space.add_tokens('generic_tokens',7)
        self.assertEqual(self.space.tokens['generic_tokens'], 7)

    def test_add_more_tokens(self):
        # checks that token count is summed if tokens exist on the space
        self.space.add_tokens('generic_tokens',2)
        self.space.add_tokens('generic_tokens',3)
        self.assertEqual(self.space.tokens['generic_tokens'], 5)

    #def test_remove_tokens(self):
    #    ''' Test that tokens are removed properly'''

    #TODO rename these test functions as something more useful.
    def test_remove_tokens_remove_all(self):
        '''tests that boardspace.BoardSpace.remove_tokens all tokens.'''
        self.space.add_tokens('generic_tokens',5)

        # check that the right number of tokens are removed
        self.assertEqual(self.space.remove_tokens('generic_tokens'),5)

        # check that that the token is removed from the tokens dict
        self.assertNotIn('generic_tokens',self.space.tokens)

    def test_remove_tokens_remove_all_by_count(self):
        '''tests that boardspace.BoardSpace.remove_tokens all tokens.'''
        self.space.add_tokens('generic_tokens',5)

        # check that the right number of tokens are removed
        self.assertEqual(self.space.remove_tokens('generic_tokens',5),5)

        # check that that the token is removed from the tokens dict
        self.assertNotIn('generic_tokens',self.space.tokens)

    def test_remove_tokens_remove_some(self):
        '''tests that boardspace.BoardSpace.remove_tokens removes the right number of
        tokens when it removes a couple of tokens.'''
        self.space.add_tokens('generic_tokens',5)

        # assert that the proper # of tokens are returned
        self.assertEqual(self.space.remove_tokens('generic_tokens',2),2)

        # assert that the proper # of tokens remain
        self.assertEqual(self.space.tokens['generic_tokens'],3)

    def test_remove_tokens_remove_too_many(self):
        ''' tests that remove_tokens throws an exception
            if too many tokens are removed'''
        self.space.add_tokens('generic_tokens',2)
        with self.assertRaises(sw_exceptions.InputError):
            self.space.remove_tokens(5)

    def test_remove_tokens_remove_wrong_key(self):
        ''' tests that remove_tokens throws an exception
 		if a bad key is suplied'''
        with self.assertRaises(sw_exceptions.InputError):
            self.space.remove_tokens('generic_token')

if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
