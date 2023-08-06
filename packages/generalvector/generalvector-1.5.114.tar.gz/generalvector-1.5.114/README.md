<details open>
<summary><h1>generalvector</h1></summary>

Simple immutable vectors.

<details>
<summary><h2>Table of Contents</h2></summary>

<pre>
<a href='#generalvector'>generalvector</a>
├─ <a href='#Dependency-Diagram-for-ManderaGeneral'>Dependency Diagram for ManderaGeneral</a>
├─ <a href='#Installation-showing-dependencies'>Installation showing dependencies</a>
├─ <a href='#Information'>Information</a>
├─ <a href='#Attributes'>Attributes</a>
├─ <a href='#Contributions'>Contributions</a>
└─ <a href='#Todo'>Todo</a>
</pre>
</details>


<details open>
<summary><h2>Dependency Diagram for ManderaGeneral</h2></summary>

```mermaid
flowchart LR
2([library]) --> 4([vector])
1([tool]) --> 2([library])
3([file]) --> 5([packager])
2([library]) --> 3([file])
0([import]) --> 2([library])
0([import]) --> 3([file])
2([library]) --> 5([packager])
click 0 "https://github.com/ManderaGeneral/generalimport"
click 1 "https://github.com/ManderaGeneral/generaltool"
click 2 "https://github.com/ManderaGeneral/generallibrary"
click 3 "https://github.com/ManderaGeneral/generalfile"
click 4 "https://github.com/ManderaGeneral/generalvector"
click 5 "https://github.com/ManderaGeneral/generalpackager"
style 4 fill:#482
```
</details>


<details open>
<summary><h2>Installation showing dependencies</h2></summary>

| `pip install`                                                        | `generalvector`   |
|:---------------------------------------------------------------------|:------------------|
| <a href='https://pypi.org/project/generallibrary'>generallibrary</a> | ✔️                |
</details>


<details open>
<summary><h2>Information</h2></summary>

| Package                                                          | Ver                                                | Latest Release        | Python                                                                                                                                                                                                                                                 | Platform        | Cover   |
|:-----------------------------------------------------------------|:---------------------------------------------------|:----------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:----------------|:--------|
| [generalvector](https://github.com/ManderaGeneral/generalvector) | [1.5.114](https://pypi.org/project/generalvector/) | 2023-06-05 11:30 CEST | [3.8](https://www.python.org/downloads/release/python-380/), [3.9](https://www.python.org/downloads/release/python-390/), [3.10](https://www.python.org/downloads/release/python-3100/), [3.11](https://www.python.org/downloads/release/python-3110/) | Windows, Ubuntu | 52.4 %  |
</details>



<details>
<summary><h2>Attributes</h2></summary>

<pre>
<a href='https://github.com/ManderaGeneral/generalvector/blob/master/generalvector/__init__.py#L1'>Module: generalvector</a>
├─ <a href='https://github.com/ManderaGeneral/generalvector/blob/master/generalvector/vector.py#L10'>Class: Vec</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalvector/blob/master/generalvector/vector.py#L122'>Method: clamp</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalvector/blob/master/generalvector/vector.py#L168'>Method: distance</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalvector/blob/master/generalvector/vector.py#L142'>Method: hex</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalvector/blob/master/generalvector/vector.py#L133'>Method: inrange</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalvector/blob/master/generalvector/vector.py#L67'>Method: length</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalvector/blob/master/generalvector/vector.py#L113'>Method: max</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalvector/blob/master/generalvector/vector.py#L104'>Method: min</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalvector/blob/master/generalvector/vector.py#L73'>Method: normalized</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalvector/blob/master/generalvector/vector.py#L88'>Method: random</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalvector/blob/master/generalvector/vector.py#L149'>Method: range</a>
│  └─ <a href='https://github.com/ManderaGeneral/generalvector/blob/master/generalvector/vector.py#L82'>Method: round</a>
└─ <a href='https://github.com/ManderaGeneral/generalvector/blob/master/generalvector/vector2.py#L9'>Class: Vec2</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalvector/blob/master/generalvector/vector2.py#L122'>Method: clamp</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalvector/blob/master/generalvector/vector2.py#L161'>Method: distance</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalvector/blob/master/generalvector/vector2.py#L132'>Method: inrange</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalvector/blob/master/generalvector/vector2.py#L67'>Method: length</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalvector/blob/master/generalvector/vector2.py#L113'>Method: max</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalvector/blob/master/generalvector/vector2.py#L104'>Method: min</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalvector/blob/master/generalvector/vector2.py#L73'>Method: normalized</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalvector/blob/master/generalvector/vector2.py#L88'>Method: random</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalvector/blob/master/generalvector/vector2.py#L143'>Method: range</a>
   └─ <a href='https://github.com/ManderaGeneral/generalvector/blob/master/generalvector/vector2.py#L82'>Method: round</a>
</pre>
</details>


<details open>
<summary><h2>Contributions</h2></summary>

Issue-creation, discussions and pull requests are most welcome!
</details>


<details>
<summary><h2>Todo</h2></summary>

| Module                                                                                                           | Message                                                                                                                                    |
|:-----------------------------------------------------------------------------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------|
| <a href='https://github.com/ManderaGeneral/generalvector/blob/master/generalvector/general.py#L1'>general.py</a> | <a href='https://github.com/ManderaGeneral/generalvector/blob/master/generalvector/general.py#L7'>Move most methods to _GeneralVector.</a> |
</details>


<sup>
Generated 2023-06-05 11:30 CEST for commit <a href='https://github.com/ManderaGeneral/generalvector/commit/master'>master</a>.
</sup>
</details>

