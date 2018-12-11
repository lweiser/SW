#!/usr/bin/env python
import sw_exceptions
class BaseSpace:
    ''' Basic Small World Space 
    ...
    
    Attributes:
    -----------
    
    neighbors : list
        List containing the ids of neighboring board spaces
        
    owner: string or None
        The player that owns the space
        
    symbol: string 
        Any special symbol on the space.
        allowed values: 'cavern','magic_source','mine',None
    
    tokens: dictionary 
        Dictionary of tokens on the space and their number
    
    terrain: string 
        The type of terrain for the space. 
        allowed values: 'farm','hills','swamp','mountains','water','edge'
        
    TODO:

    Implement a graphical representation? 
        
    '''
    
    # I am not sure about the choice to make this global? 
    
    def add_tokens(self,token:str,count:int):
        '''Adds tokens to a smallworld space.
        
        Args:
            token: string token descriptor
            count: integer number of tokens to add
        
        Returns:
            Updates self.tokens dictionary with the {token : count}
            {key : value pair}'''
        
        self.__check_less_than_integer(count,1)
      
        # if the token already on space, add to its count
        if token in self.tokens: 
            self.tokens[token] += count 
        
        # otherwise add the token and count together
        else: 
            self.tokens[token] = count
            
            
    def remove_tokens(self,token:str,count=None):
        ''' Removes tokens of type token 'token' from the dict.
            
            inputs: token: string of the token name
                    counts: None - remove all toens
                            int-remove that number of tokens'''
        
        if token not in self.tokens:
            ## TODO: throw an error to prevent call? 
            raise sw_exceptions.InputError(
                    'Token {} could not be removed, not on space.'.format(token))
        
        # return all tokens if count set to None
        elif count is None:
            return self.tokens.pop(token,None) # return tokens to user
          
        elif count > self.tokens[token]:
            # TODO: change this to a custom exception later? 
            raise sw_exceptions.InputError(
                    'Cannot remove more tokens ({})than on space ({})'.format(
                            count, self.tokens[token]))
        # remove count tokens if possible
        elif count == self.tokens[token]:
            # pop the key from the dictionary to remove everything
            return self.tokens.pop(token,None) # return tokens to user
        
        else:
            self.tokens[token] -= 2
            return count
        
    def change_owner(self,new_owner=None):
        '''Changes the owner of the space.
        
        Does this function fit python style conventions? Regarding: encapsulation'''
        
        # TODO: Write a restriction on input
        if ( not None ) and ( not isinstance(new_owner,str)):
            raise sw_exceptions.InputError('Change_owner requires a string as input.')
            
        else: self.owner = new_owner
            
    def add_neighbor(self,neighbor_id:int):
        ''' adds the neighbor_id to the neighbor_list'''
        
        self.__check_less_than_integer(neighbor_id,0)
            
        self.neighbors.append(neighbor_id)
            
    def __check_less_than_integer(self, value, cutoff = 0):
        '''helper function to check if value is a positive integer'''
        if not isinstance(value,int):
            raise TypeError('Invalid value: {}! Must be an integer!'.format(value))
        
        if value < cutoff:
            raise sw_exceptions.InputError(
                    'Illegal value: {}! Must be less than: {} !'.format(value,cutoff))
    
    def __check_init_inputs(self,space_id,terrain,lost_tribes,map_symbol):
        ''' This function raises assertions for all input errors'''
        
        __terrain_types = set(['farm','hills','mountains','swamp','water'])
        __map_symbols = set(['cavern','magic','mine'])
    
        if terrain not in __terrain_types:
            raise sw_exceptions.InputError('Invalid terrain type: {}'.format(terrain))
            
        if (space_id < 1):
            raise sw_exceptions.InputError("Space ID must be positive")
                
        if not isinstance(lost_tribes,bool):
            raise TypeError('lost_tribes:{} invalid! Must be a bool!'.format(lost_tribes))
            
        if not isinstance(space_id,int):
            raise TypeError('ID:({}) invalid! Must be an integer!'.format(space_id))
            
        if ((map_symbol is not None) and (map_symbol not in __map_symbols)):
                raise sw_exceptions.InputError('Invalid map symbol: {}'.format(map_symbol))
                
        if (terrain =='mountains') and (lost_tribes != False):
                raise sw_exceptions.InputError(
                        '\'lost_tribes\' not permitted on \'mountains\' terrain' )
                
        if not isinstance(edge,bool):
            raise TypeError('edge:{} invalid! Must be a bool!'.format(edge))

    def __init__(self,space_id:int,terrain:str,edge=True,
                 lost_tribes=False,map_symbol=None):  
        '''Initializes the BaseSpace
        Args: space_id - integer id of the space
        
              terrain - string from list [mountains, swamp, farm, hills, edge, water]
              
              edge - True if an edge space, false otherwise.
              
              lost_tribes - bool indicating if lost_tribes are present
              
              map_symbol - string from list ['magic_source','mine','cavern']
        
        Output: object of type BaseSpace '''
        
        
        # not sure if I should use this underscore syntax
       
        
        # check for input error
        self.__check_init_inputs(space_id,terrain, lost_tribes, map_symbol)
        
        # intialize the neighbors and tokens lists
        self.neighbors = [] 
        self.tokens = {} # key = types of space tokens, value = their number
        
        # initialize neighbor_list
        self.neighbors = []
        
        # initialize terrain
        self.terrain = terrain
        
        # initialize symbol
        self.symbol = map_symbol      
        
        # I'm not sure that I need both of these
        self.name = 'Space_{}'.format(space_id)
        self.id = space_id    
        self.is_edge=edge
        
        # Is this the best way to bookkeep the owner?
        if lost_tribes is False:
            self.owner = None
        else:
            self.owner = 'lost_tribes'
            self.add_tokens('lost_tribes',2)
        
        if terrain == 'mountains':
            self.add_tokens('mountains',1)      
    def __repr__(self):
        #TODO: Have this print out useful information:
        # .    e.g.: Owner Tokens(if onwer)
        # .          Other TOkens (if other)
        #      Under Special Power ( if needed)
        # .    Total Tokens
        
        #name_id='name: {}\n  id: {}\n'.format(self.name, self.id)
        name_id='Space: {}\n'.format(self.id)
        
        if self.owner is not None:
            owner_info = 'owner: {}\n  owner_tokens: {} \n'.format(self.owner, self.tokens[self.owner])
        else:
            owner_info = 'owner: None\n  owner_tokens: 0\n'
            
        terrain_info = 'terrain: {} \nsymbol: {} \n'.format(self.terrain,self.symbol)
        
        tokens_info ='tokens: \n'
        for key,value in self.tokens.items():
            tokens_info += '  {} : {}\n'.format(key,value)
        
        # TODO: Implement the print for this
        neighbor_info ='neighbors: \n'
        for neighbor  in self.neighbors:
            neighbor_info += '  {} '.format(neighbor)
        
        # TODO implement the dictionary print
        
        return ''.join([name_id,owner_info,terrain_info,tokens_info,neighbor_info])

