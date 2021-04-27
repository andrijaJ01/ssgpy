# Static site generator

A basic static site generator written in Python for learning purposes.
It generates the blog styled with bootstrap

# Requirements

- python 3
- jinja2 package
- markdown2 package
- git

# How to create Post?

To create content first create markdown page for it in ```content/``` directory.

next is to add metadata to the article:

- title
- subtitle
- summary
- author
- date in format YYYY-MM-DD
- headerimg (image for the header section of post page)

example post
```
---
headerimg:assets/img/0131.jpg
title: Turkish Cheese Pide
subtitle: test
date: 2019-04-12
tags: Bread, Savoury
thumbnail: img/pide.jpg
summary: Traditional Turkish pide stuffed with cheese. Great as an appetizer or for breakfast or lunch.
slug: turkish-pide
author: Andrija Jovanovic
---

__Ingredients__

+ 500gm bread flour
+ 1 tblspoon yeast
+ 1 tblspoon honey
+ 1 tsp salt
+ 2 tblsp olive oil
+ 250 ml or as req water.

**Ingredients for the filling:**

+ 1 cup grated Mozerella
+ ½ cup crumbled feta 

__Preparation__
 
Combine the ingredients of the dough and knead until smooth and elastic. Let rest 45 minutes. Divide in two for two large pides or into four for four medium sized pides. Roll each in a rectangle. Spread the cheese filling over top. And roll the sides in to form a boat shape. Let rise for 10-15 minutes. Brush the sides with olive oil and bake at 230C for 10-15 minutes or until nicely browned.
```
