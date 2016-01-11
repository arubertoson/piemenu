#!/usr/bin/env python
# -*- coding: utf-8 -*-

text = '    long weird string with cahracters'
print text.lstrip()
print text[:len(text)-len(text.lstrip())]
