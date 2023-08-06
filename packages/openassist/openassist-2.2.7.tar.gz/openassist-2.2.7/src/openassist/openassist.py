# OpenAssist v2.2.7 - FZ#2023
# OpenAssist is a module for Python that allows you to create an AI assistant using import openai with ease.

# Usage:

# ROLES :                  'system' = System Guide, 'assistant' = Ai Assistant, 'user' = User
# DEFAULT GPT DICT :       {'role': 'system', 'content': 'You are a friendly assistant.'}
# DEFAULT ROLES FILE :     'roles.txt'
# COMING SOON :            Parameters to be added to chat_completion() and completion() functions (temperature, top_p, max_tokens, stop) etc,..

"""
Example Of Importing -
    import openassist as OpenAssist - Import the module as OpenAssist
    or
    from openassist import OpenAIResponse, Roles, Memory - Import the classes individually (note case sensitivity)

Example Of Initializing Classes -
    Memory1 = OpenAssist.Memory() - Initialize the memory list
    Roles = OpenAssist.Roles("roles.txt") - Initialize the roles list with the specified file/path

Example Of OpenAI Completions -
    OpenAIRes = OpenAssist.OpenAIResponse(api_key, model_id="gpt-4") - Initialize the OpenAIResponse class (model_id is optional but defaults to gpt-4)
    OpenAIRes.chat_completion(Memory1.return_list()) - Run the OpenAI Chat Completion function
    OpenAIRes.completion(prompt, max_tokens=150) - Run the OpenAI Completion function

OpenAIResponse -
    chat_completion(memory_list, max_tokens=150) - Run the OpenAI Chat Completion function
    completion(prompt, max_tokens=150) - Run the OpenAI Completion function (max_tokens is optional but defaults to 100)

Roles -
    [Roles.] - Instance Name
    add(role_name, role_content, as_role) - Add a role to the roles list
    remove(role_name) - Remove a role from the roles list
    view() - View the roles list
    select(role_name) - Get a selected role from the roles list
    random() - Get a random role from the roles list
    format(role, content) - Format content into a role dictionary (role can be 'system', 'assistant', or 'user')

Memory -
    [Memory1.] - Instance Name
    add(dictionary) - Add a dictionary to the memory list
    remove(dictionary) - Remove a dictionary from the memory list
    remove_index(index) - Remove a dictionary from the memory list in the specified index
    insert(index, dictionary) - Insert a dictionary into the memory list at the specified index
    clear() - Clear the memory list
    view_list() - View the memory list
    return_list() - Return the memory list
    edit(dictionary, index) - Edit a dictionary in the memory list at the specified index
    get_index(dictionary) - Get the index of a dictionary in the memory list
"""

# Import modules
import random, openai

# OpenAssist.OpenAIResponse
class OpenAIResponse:
    def __init__(self, api_key, model_id="gpt-4"):
        """
        Initialize the OpenAIResponse class.
        
        api_key - Your OpenAI API key.
        model_id - The model ID to use for the OpenAI Completion function.
        """

        try:
            self.api_key = api_key
            self.model_id = model_id

            if not isinstance(self.api_key, str) or not isinstance(self.model_id, str):
                raise ValueError("API key and model ID must be strings.")
            if not self.api_key or not self.model_id:
                raise ValueError("API key and model ID cannot be empty.")

            openai.api_key = self.api_key
        except Exception as e:
            raise Exception(f"Unexpected error: {e}")

    # OpenAssist.OpenAIResponse.functions - OpenAIResponse.chat_completion(), OpenAIResponse.completion()

    def chat_completion(self, memory_list, max_tokens=150):
        """
        Run the OpenAI Chat Completion function.
        
        memory_list - The memory list to use for the chat completion.
        """

        try:
            if not isinstance(memory_list, list):
                raise ValueError("Memory list must be a list.")
            if not memory_list:
                raise ValueError("Memory list cannot be empty.")
            if not isinstance(max_tokens, int):
                raise ValueError("Max tokens must be an integer.")

            try:
                response = openai.ChatCompletion.create(
                    model=self.model_id,
                    messages=memory_list,
                    max_tokens=max_tokens
                )
            except openai.error.OpenAIError as e:
                raise Exception(f"OpenAI error: {e}")
            except Exception as e:
                raise Exception(f"Unexpected error: {e}")

            try:
                return response.choices[0].message.content
            except (AttributeError, IndexError):
                raise Exception("Unexpected response structure from API.")
        except Exception as e:
            raise Exception(f"Unexpected error: {e}")
    
    def completion(self, prompt, max_tokens=150):
        """
        Run the OpenAI Completion function.
        
        prompt - The prompt to use for the completion.
        max_tokens - The maximum number of tokens to generate.
        """

        try:

            if not isinstance(prompt, str):
                raise ValueError("Prompt must be a string.")
            if not prompt:
                raise ValueError("Prompt cannot be empty.")
            if not isinstance(max_tokens, int):
                raise ValueError("Max tokens must be an integer.")
            
            try:
                response = openai.Completion.create(
                    engine=self.model_id,
                    prompt=prompt,
                    max_tokens=max_tokens
                )
            except openai.error.OpenAIError as e:
                raise Exception(f"OpenAI error: {e}")
            except Exception as e:
                raise Exception(f"Unexpected error: {e}")
            
            try:
                return response.choices[0].text
            except (AttributeError, IndexError):
                raise Exception("Unexpected response structure from API.")
        except Exception as e:
            raise Exception(f"Unexpected error: {e}")

# OpenAssist.Roles
class Roles:

    def __init__(self, file='roles.txt'):
        """
        Initialize the Roles class.
        
        file - The file to use for the roles list.
        """

        try:
            self.roles = []
            self.file = file
            
            try:
                role_list_raw = open(self.file, 'r').readlines()
            except FileNotFoundError:
                raise ValueError(f'{self.file} not found.')
            except Exception as e:
                raise Exception(f'Error: {e}')
            
            # Remove \n from role_list_raw and update it
            for i in range(len(role_list_raw)):
                role_list_raw[i] = role_list_raw[i].replace('\n', '')

            # Search for roles in the roles folder and add them to the roles list
            for role in role_list_raw:
                name = role.split(':', 1)[0]
                content = role.split(':', 1)[1]
                self.roles.append({'role': 'system', 'content': content, 'role_name': name})
        except Exception as e:
            raise Exception(f'Error: {e}')

    # OpenAssist.Roles.functions - Roles.format(), Roles.add(), Roles.remove(), Roles.view(), Roles.select(), Roles.random()
    
    # Format the given content to a role dictionary
    def format(self, role, content):
        """
        Format the given content to a role dictionary.
        
        role - The role type.
        content - The content of the role.
        """

        try:
            if role == 'user' or role == 'system' or role == 'assistant' and type(content) == str:
                return {'role': f'{role}', 'content': content}
            elif role != 'user' and role != 'system' and role != 'assistant':
                raise ValueError(f'Error: Roles.format() - Invalid role type: {role}.')
            elif type(content) != str:
                raise ValueError(f'Error: Roles.format() - {content} is not a string.')
            else:
                raise Exception(f'Error: Roles.format() - {role} is not a string.')
        except Exception as e:
            raise Exception(f'Error: {e}')
    
    # Add a role to the roles list
    def add(self, role_name, role_content, as_role='system'):
        """
        Add a role to the roles list.

        role_name - The name of the role.
        role_content - The content of the role.
        as_role - The role type. Default is system.
        """

        try:
            role_to_add_exists = False

            for role in self.roles:
                if role['role_name'] == role_name:
                    role_to_add_exists = True
                else:
                    continue
            
            if role_to_add_exists:
                raise ValueError(f'Error: Roles.add() - Role {role_name} already exists.')
            else:
                if as_role == 'user' or as_role == 'system' or as_role == 'assistant':
                    self.roles.append({'role': f'{as_role}', 'content': role_content, 'role_name': role_name})
                elif as_role != 'user' and as_role != 'system' and as_role != 'assistant':
                    raise ValueError(f'Error: Roles.add() - Invalid role type: {as_role}.')
                else:
                    raise Exception(f'Error: Roles.add() - {as_role} is not a string.')
        except Exception as e:
            raise Exception(f'Error: {e}')

    # Remove a role from the roles list
    def remove(self, role_name):
        """
        Remove a role from the roles list.
        
        role_name - The name of the role.
        """

        try:
            role_to_remove = []

            for role in self.roles:
                if role['role_name'] == role_name:
                    role_to_remove.append(role)
                else:
                    continue

            if role_to_remove == []:
                raise ValueError(f'Error: Roles.remove() - No role named {role_name} found.')
            else:
                for role in role_to_remove:
                    self.roles.remove(role)
        except Exception as e:
            raise Exception(f'Error: {e}')
        
    # View the roles list
    def view(self):
        """
        View the roles list.
        """

        try:
            role_to_return = []
            for role in self.roles:
                role_to_return.append(role['role_name'])
            print(role_to_return)
        except Exception as e:
            raise Exception(f'Error: {e}')

    # Get a selected role from the roles list
    def select(self, role_name):
        """
        Get a selected role from the roles list.
        
        role_name - The name of the role.
        """

        try:
            role_to_return = []
            for role in self.roles:
                if role['role_name'] == role_name:
                    role_to_return.append(role)
                else:
                    continue

            if role_to_return == []:
                raise ValueError(f'Error: Roles.select() - No role named {role_name} found.')
            else:
                # pop role_name from role_to_return
                role_to_return[0].pop('role_name')
                return dict(role_to_return[0])
        except Exception as e:
            raise Exception(f'Error: {e}')

    # Get a random role from the roles list
    def random(self):
        """
        Get a random role from the roles list.
        """

        try:
            chosen_role = random.choice(self.roles)
            return {'role': chosen_role['role'], 'content': chosen_role['content']}
        except IndexError:
            raise Exception('Error: Roles.random() - No roles found.')
        except Exception as e:
            raise Exception(f'Error: {e}')

# OpenAssist.Memory
class Memory:

    # OpenAssist.Memory = OpenAssist.Memory()
    def __init__(self):
        """
        Initialize the Memory class.
        """

        try:
            self.memory = []
        except Exception as e:
            raise Exception(f'Error: {e}')

    # OpenAssist.Memory.functions - Memory.add(), Memory.remove(), Memory.remove_index(), Memory.insert(), Memory.clear(), Memory.view(), Memory.return_()

    # Add a dictionary to the memory list
    def add(self, dictionary):
        """
        Add a dictionary to the memory list.
        
        dictionary - The dictionary to add.
        """

        try:
            if type(dictionary) != dict and dictionary != None:
                raise ValueError(f'Error: Memory.add() - {dictionary} is not a dictionary.')
            elif dictionary == None:
                raise ValueError(f'Error: Memory.add() - Cannot Add None.')
            else:
                self.memory.append(dictionary)
        except ValueError as e:
            raise ValueError(f'Error: Memory.add() - {e}')

    # Remove a dictionary from the memory list
    def remove(self, dictionary):
        """
        Remove a dictionary from the memory list.
        
        dictionary - The dictionary to remove.
        """

        try:
            if type(dictionary) != dict and dictionary != None:
                raise ValueError(f'Error: Memory.remove() - {dictionary} is not a dictionary.')
            elif dictionary == None:
                raise ValueError(f'Error: Memory.remove() - Cannot Remove None.')
            else:
                self.memory.remove(dictionary)
        except ValueError as e:
            raise ValueError(f'Error: Memory.remove() - {e}')

    # Get a dictionary from the memory list at a specified index
    def get_index(self, index):
        """
        Get a dictionary from the memory list at a specified index.
        
        index - The index of the dictionary to get.
        """

        try:
            if not index < -len(self.memory) and not index >= len(self.memory):
                try:
                    return self.memory[index]
                except (ValueError, TypeError) as e:
                    raise ValueError(f'Error: Memory.get_index() - Invalid index: {index}. {str(e)}')
                except IndexError:
                    raise ValueError(f'Error: Memory.get_index() - Index out of range: {index}')
                except Exception as e:
                    raise Exception(f'Error: Memory.get_index() - {e}')
            else:
                raise ValueError(f'Error: Memory.get_index() - Index out of range: {index}')
        except ValueError as e:
            raise ValueError(f'Error: Memory.get_index() - {e}')

    # Remove a dictionary from the memory list in the specified index
    def remove_index(self, index):
        """
        Remove a dictionary from the memory list in the specified index.
        
        index - The index of the dictionary to remove.
        """

        try:
            if not index < -len(self.memory) and not index >= len(self.memory):
                try:
                    self.memory.remove(self.memory[index])
                except (ValueError, TypeError) as e:
                    raise ValueError(f'Error: Memory.remove_index() - Invalid index: {index}. {str(e)}')
                except IndexError:
                    raise ValueError(f'Error: Memory.remove_index() - Index out of range: {index}')
                except Exception as e:
                    raise Exception(f'Error: Memory.remove_index() - {e}')
            else:
                raise ValueError(f'Error: Memory.remove_index() - Index out of range: {index}')
        except ValueError as e:
            raise ValueError(f'Error: Memory.remove_index() - {e}')

    # Insert a dictionary into the memory list at the specified index
    def insert(self, index, dictionary):
        """
        Insert a dictionary into the memory list at the specified index.
        
        index - The index to insert the dictionary at.
        dictionary - The dictionary to insert.
        """

        try:
            if not index < -len(self.memory) and not index >= len(self.memory):
                if type(dictionary) != dict and dictionary != None:
                    raise ValueError(f'Error: Memory.insert() - {dictionary} is not a dictionary.')
                elif dictionary == None:
                    raise ValueError(f'Error: Memory.insert() - Cannot Insert None.')
                elif type(index) != int:
                    raise ValueError(f'Error: Memory.insert() - {index} is not an integer.')
                else:
                    try:
                        self.memory.insert(index, dictionary)
                    except (ValueError, TypeError) as e:
                        raise ValueError(f'Error: Memory.insert() - Invalid index: {index}. {str(e)}')
                    except IndexError:
                        raise ValueError(f'Error: Memory.insert() - Index out of range: {index}')
                    except Exception as e:
                        raise Exception(f'Error: Memory.insert() - {e}')
            else:
                raise ValueError(f'Error: Memory.insert() - Index out of range: {index}')
        except Exception as e:
            raise Exception(f'Error: Memory.insert() - {e}')

    # Edit a dictionary in the memory list at the specified index
    def edit(self, index, new_role, new_content):
        """
        Edit a dictionary in the memory list at the specified index.
        
        index - The index of the dictionary to edit.
        new_role - The new role to set.
        new_content - The new content to set.
        """

        try:
            if type(index) != int:
                raise ValueError(f'Error: Memory.edit() - {index} is not an integer.')
            elif type(new_role) != str:
                raise ValueError(f'Error: Memory.edit() - {new_role} is not a string.')
            elif type(new_content) != str:
                raise ValueError(f'Error: Memory.edit() - {new_content} is not a string.')
            else:
                if not index < -len(self.memory) and not index >= len(self.memory):
                    try:
                        self.memory[index]['role'] = new_role
                        self.memory[index]['content'] = new_content
                    except (ValueError, TypeError) as e:
                        raise ValueError(f'Error: Memory.edit() - Invalid index: {index}. {str(e)}')
                    except IndexError:
                        raise ValueError(f'Error: Memory.edit() - Index out of range: {index}')
                    except Exception as e:
                        raise Exception(f'Error: Memory.edit() - {e}')
                else:
                    raise ValueError(f'Error: Memory.edit() - Index out of range: {index}')
        except Exception as e:
            raise Exception(f'Error: Memory.edit() - {e}')

    # Clear the memory list
    def clear(self):
        """
        Clear the memory list.
        """

        try:
            Memory.memory = []
            self.memory = Memory.memory
        except Exception as e:
            raise Exception(f'Error: Memory.clear() - {e}')

    # Return the memory list
    def return_list(self):
        """
        Return the memory list.
        """

        try:
            return self.memory
        except Exception as e:
            raise Exception(f'Error: Memory.return_list() - {e}')

    # View the memory list
    def view_list(self):
        """
        View the memory list.
        """

        try:
            print(self.memory)
        except Exception as e:
            raise Exception(f'Error: Memory.view_list() - {e}')

# For testing purposes
if __name__ == '__main__':
    pass
