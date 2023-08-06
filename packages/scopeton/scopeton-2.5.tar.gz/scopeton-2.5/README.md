# Scopeton

Scopeton is a simple dependency injection framework for Python inspired by the Java Spring framework

Main entities of the scopeton:

* Scope - the context of the application
* Bean - the small brick of the application to inject, can be singleton (default) or multiton

## Installation

```pip install scopeton```

## Basic usage

Firstly you have to create a scope and register beans there:

```python
from scopeton import scope
class Dependency1:
    pass
class Dependency2:
    pass
class Dependency3:
    pass
appScope = scope.Scope()
appScope.registerBean(Dependency1, Dependency2, Dependency3)
```

There are several ways how to get the instance of dependency from the scope:
1. Service locator style: 
```python
    depencency1Instance = appScope.getInstance(Dependency1) - returns the singleton instance of Dependency1  
```
2. Automatic constructor injection:
```python
from scopeton import scope
from scopeton.decorators import Inject

class Dependency1():
    pass

class Dependency4():
    pass

class Dependency5():
    @Inject()
    def __init__(self, dep1: Dependency1, a):
        pass


class Dependency7():
    called = False
    @Inject()
    def __init__(self, dep1:Dependency1, dep4: Dependency4):
        assert isinstance(dep1, Dependency1)
        assert isinstance(dep4, Dependency4)
        
appScope = scope.Scope()
appScope.registerBean(Dependency1, Dependency4, Dependency5, Dependency7)
instance = appScope.getInstance(Dependency7)

```
in this case the Dependency1 and Dependency4 will be injected automatically to the constructor of the Dependency7


## Beans

The default bean configuration 

```python
appScope.registerBean(Dependency1, Dependency2, Dependency3)
```
configures beans Dependency1, Dependency2, Dependency3
with lazy = False, singleton=True, service = True

overriding bean parameters:
```python
appScope.registerBean(Bean(Dependency1, singleton = False), Dependency2, Dependency3)
```
in this case Dependency1 will be non-singleton bean

## Services
All beans can have postConstruct and preDestroy functions, these functions will be called automatically:
postConstruct will be called for each bean after 
```python
appScope.runServices()
```
and preDestroy will be called after 
```python
appScope.stopServices()
```

## Inject scope

Each bean can inject the scope itself (avoiding circular dependencies)

```python
class Dependency():
    @Inject()
    def __init__(self, scope: Scope, a):
        self
```

