Terraply
========

A thin terraform wrapper that expands the -target argument using glob syntax and adds an -exclude
argument.


## Install

You must have terraform installed. Then:

```
pip install terraply
```

## Examples
```
terraply apply -target module.child-module-*.resource
```


```
terraply apply -target module.child-module-*.resource --exclude module.child-module-5
```
