
# coding: utf-8

# In[1]:


import pycparser


# In[31]:


ast = pycparser.parse_file("x.cc", use_cpp=True)
one_arg = ast.children()[0][1].children()[1][1].children()
two_args = ast.children()[1][1].children()[1][1].children()
three_args = ast.children()[2][1].children()[1][1].children()
multiple_args = ast.children()[3][1].children()[1][1].children()
conversions = ast.children()[4][1].children()[1][1].children()
assignments = ast.children()[5][1].children()[1][1].children()


# In[26]:


funcs = []


# In[22]:


for entry in one_arg:
    func = {}
    if type(entry[1].children()[1][1]) is pycparser.c_ast.ID:
        func["name"] = entry[1].children()[1][1].name
    else:
        func["name"] = entry[1].children()[1][1].value
    if type(entry[1].children()[3][1]) is pycparser.c_ast.ID:
        func["arguments"] = [entry[1].children()[3][1].name]
    else:
        func["arguments"] = [entry[1].children()[3][1].value]
    if type(entry[1].children()[2][1]) is pycparser.c_ast.ID:
        func["res"] = entry[1].children()[2][1].name
    else:
        func["res"] = entry[1].children()[2][1].value
    funcs.append(func)


# In[ ]:


for entry in two_args:
    func = {}
    if type(entry[1].children()[1][1]) is pycparser.c_ast.ID:
        func["name"] = entry[1].children()[1][1].name
    else:
        func["name"] = entry[1].children()[1][1].value
        
    if type(entry[1].children()[3][1]) is pycparser.c_ast.ID:
        func["arguments"] = [entry[1].children()[3][1].name]
    else:
        func["arguments"] = [entry[1].children()[3][1].value]
        
    if type(entry[1].children()[4][1]) is pycparser.c_ast.ID:
        func["arguments"].append(entry[1].children()[4][1].name)
    else:
        func["arguments"].append(entry[1].children()[4][1].value)
        
    if type(entry[1].children()[2][1]) is pycparser.c_ast.ID:
        func["res"] = entry[1].children()[2][1].name
    else:
        func["res"] = entry[1].children()[2][1].value
        
    funcs.append(func)


# In[ ]:


for entry in three_args:
    func = {}
    if type(entry[1].children()[1][1]) is pycparser.c_ast.ID:
        func["name"] = entry[1].children()[1][1].name
    else:
        func["name"] = entry[1].children()[1][1].value
        
    if type(entry[1].children()[3][1]) is pycparser.c_ast.ID:
        func["arguments"] = [entry[1].children()[3][1].name]
    else:
        func["arguments"] = [entry[1].children()[3][1].value]
        
    if type(entry[1].children()[4][1]) is pycparser.c_ast.ID:
        func["arguments"].append(entry[1].children()[4][1].name)
    else:
        func["arguments"].append(entry[1].children()[4][1].value)
        
    if type(entry[1].children()[5][1]) is pycparser.c_ast.ID:
        func["arguments"].append(entry[1].children()[5][1].name)
    else:
        func["arguments"].append(entry[1].children()[5][1].value)
        
    if type(entry[1].children()[2][1]) is pycparser.c_ast.ID:
        func["res"] = entry[1].children()[2][1].name
    else:
        func["res"] = entry[1].children()[2][1].value
        
    funcs.append(func)


# In[ ]:


# ok this is a weird one, gonna have to double check on that
for entry in multiple_args:
    func = {}
    if type(entry[1].children()[1][1]) is pycparser.c_ast.ID:
        func["name"] = entry[1].children()[1][1].name
    else:
        func["name"] = entry[1].children()[1][1].value


# In[34]:


for entry in conversions:
    func = {}
    if type(entry[1].children()[0][1]) is pycparser.c_ast.ID:
        func["arguments"] = [entry[1].children()[0][1].name]
    else:
        func["arguments"] = [entry[1].children()[0][1].value]
        
    if type(entry[1].children()[1][1]) is pycparser.c_ast.ID:
        func["res"] = entry[1].children()[1][1].name
    else:
        func["res"] = entry[1].children()[1][1].value
        
    func["name"] = func["arguments"][0] + "_to_" + func["res"]
    funcs.append


# In[35]:


for entry in assignments:
    func = {}
    if type(entry[1].children()[2][1]) is pycparser.c_ast.ID:
        func["arguments"] = [entry[1].children()[2][1].name]
    else:
        func["arguments"] = [entry[1].children()[2][1].value]
        
    if type(entry[1].children()[1][1]) is pycparser.c_ast.ID:
        func["res"] = entry[1].children()[1][1].name
    else:
        func["res"] = entry[1].children()[1][1].value
        
    func["name"] = func["arguments"][0] + "_assign_to_" + func["res"]
    funcs.append(func)

print(funcs)
