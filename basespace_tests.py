#!/usr/bin/env python
import basespace
import unittest
class TestSpaceInit_Basics(unittest.TestCase):
    def setUp(self):
        self.space = BaseSpace(1,'farm')
    
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
            with self.assertRaises(InputError):
                BaseSpace(1,t,False,None)
                
    def test_symbol_restriction_on_swamps(self):
        '''Tests that an exception is raised for symbol spelling errors'''
        for s in ['MagicSource','lost_tribes','swamps']:
            # with is used here because 
            # this sets up and tares down the class every time.
            with self.assertRaises(InputError):
                BaseSpace(1,'swamps',False,s)
    
    def test_no_lost_tribes_on_mountains(self):
        '''Tests that exception is raised for lost_tribes placed on mountains '''
        with self.assertRaises(InputError):
            BaseSpace(1,'mountains',True,None)
            
    def test_lost_tribes_exception_None(self):
        '''Tests that lost_tribes throws an error when set to None '''
        with self.assertRaises(TypeError):
            BaseSpace(1,'swamp',None,None)
        
    def test_lost_tribes_exception_one(self):
        '''Tests that lost_tribes throws an error when set to an int '''
        with self.assertRaises(TypeError):
            BaseSpace(1,'swamp',1,None)
            
    def test_lost_tribes_exception_zero(self):
        '''Tests that lost_tribes throws an error when set to an int '''
        with self.assertRaises(TypeError):
            BaseSpace(1,'swamp',0,None)
        
    def test_lost_tribes_exception_string(self):
        '''Tests that lost_tribes throws an error when set to a string'''
        with self.assertRaises(TypeError):
            BaseSpace(1,'swamp','lost_tribes',None)
        
    
    def test_no_zero_id(self):
        '''Tests that exception is raised for space_id set to 0'''
        with self.assertRaises(InputError):
            BaseSpace(0,'swamp',None,None)
            
    def test_no_negative_id(self):
        '''Tests that exception is raised for negative space ids'''
        with self.assertRaises(InputError):
            BaseSpace(-1,'swamp',None,None)
            
    def test_no_string_id(self):
        '''Tests that string ids raise an exception'''
        with self.assertRaises(TypeError):
            BaseSpace('a','swamp',None,None)
            
    def test_no_float_id(self):
        '''Tests that float ids raise an exception'''
        with self.assertRaises(TypeError):
            BaseSpace(1.4,'swamp',None,None)
            


# this code for error handling was found at https://docs.python.org/2/tutorial/errors.html
class Error(Exception):
    """Base Class for Exceptions in this module"""
    pass

class InputError(Error):
    """Exception raised for errors in the input.

    Attributes:
        expr -- input expression in which the error occurred
        msg  -- explanation of the error
    """
    def __init__(self, msg):
        self.msg = msg

class TestSpaceInit_LostTribes(unittest.TestCase):
    """Tests space initialization for lost tribes"""

    def setUp(self):
        self.space = BaseSpace(1,'swamp',True,None)       
        
    def test_lost_tribes_sets_owner(self):
        '''Tests that lost_tribes option adds properly'''
        self.assertEqual(self.space.owner,'lost_tribes')
    
    def token_count_lost_tribes(self):
        '''Tests that 2 'lost_tribes' tokens are added '''
        self.assertEqual(self.space.tokens['lost_tribes']==2)

class TestSpaceInit_Mountains(unittest.TestCase):
    """ Tests initialization issues specific to mountain spaces """

    def setUp(self):
        self.space = BaseSpace(1,'mountains')
    
    def test_terrain_name(self):
        '''tests that space.terrain is set to 'mountains''' 
        self.assertEqual(self.space.terrain,'mountains')
    
    def test_token_dict_membership(self):
        '''tests that the 'mountains' value is added to the tokens dict'''
        self.assertIn('mountains', self.space.tokens)
        
    def test_token_count(self):
        '''Tests that setup assigns 1 mountain token'''
        self.assertEqual(self.space.tokens['mountains'],1)

class TestSpaceFunctions(unittest.TestCase):
    '''Tests a few of the smaller space functions'''
    def setUp(self):
        # i'll initialize this one with a different set of test cases
        self.space = BaseSpace(1, 'farm')
    
    
    # tests for the add_tokens function
    def test_add_tokens_negative_value(self):
        '''Tests if assigning negative token values leads to error'''
        with self.assertRaises(InputError):
            self.space.add_tokens('generic_tokens',-5)
    
    def test_add_tokens_zero_values(self):
        '''Tests if assigning 0 tokens leads to error'''
        with self.assertRaises(InputError):
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
    
    # tests for the add_neighbor function
    
    def test_add_neighbor_float_error(self):
        ''' tests that the neighbor function throws a type error for floats'''
        with self.assertRaises(TypeError):
            self.space.add_neighbor(3.5)
    
    def test_add_neighbor_negative_error(self):
        ''' tests that the neighbor function throws an input error for negative'''
        with self.assertRaises(InputError):
            self.space.add_neighbor(-5)
            
    #def test_remove_tokens(self):
    #    ''' Test that tokens are removed properly'''
    
    def test_remove_tokens_remove_all(self):
        '''tests that BaseSpace.remove_tokens all tokens.'''
        self.space.add_tokens('generic_tokens',5)
        
        # check that the right number of tokens are removed
        self.assertEqual(self.space.remove_tokens('generic_tokens'),5)
        
        # check that that the token is removed from the tokens dict
        self.assertNotIn('generic_tokens',self.space.tokens)
        
    def test_remove_tokens_remove_all_by_count(self):
        '''tests that BaseSpace.remove_tokens all tokens.'''
        self.space.add_tokens('generic_tokens',5)
        
        # check that the right number of tokens are removed
        self.assertEqual(self.space.remove_tokens('generic_tokens',5),5)
        
        # check that that the token is removed from the tokens dict
        self.assertNotIn('generic_tokens',self.space.tokens)
        
        
    def test_remove_tokens_remove_some(self):
        '''tests that BaseSpace.remove_tokens removes the right number of
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
        with self.assertRaises(InputError):
            self.space.remove_tokens(5)
            
    def test_remove_tokens_remove_wrong_key(self):
        ''' tests that remove_tokens throws an exception 
 		if a bad key is suplied'''
        with self.assertRaises(InputError):
            self.space.remove_tokens('generic_token')
            
if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)

