# Evolution of searchtools.js

This document tracks the evolution of `searchtools.js` in the Sphinx project, based on its git history from 2007 to 2024.

## Timeline Overview

**Total commits affecting searchtools.js: 77+**
**Timespan: July 2007 - May 2024**

## Major Milestones

### 2007-2009: Foundation Era
- **July 2007** - Initial import as part of the Sphinx documentation tools (commit d60ca8d49)
- **2008** - Basic search functionality established with jQuery dependency
- **2009** - Object name searching support (`sys.argv` style searches)

### 2010-2012: Feature Expansion
- **2010** - jQuery 1.4 compatibility and Internet Explorer fixes
- **2011** - Multi-word search improvements and object lookup enhancements
- **2012** - Japanese language support and pluggable search scoring system

### 2013-2017: Refinement Period
- **2013** - Partial matching support for search terms
- **2014-2015** - HTML preview snippets and search result improvements
- **2016** - Source file suffix configuration and template compatibility
- **2017** - Reader-friendly HTML search results

### 2018-2021: Modern JavaScript Era
- **2018** - Search result highlighting and CSS improvements
- **2019** - Type-dependent search results and relevance scoring enhancements
- **2020** - Multiple bug fixes and edge case handling
- **2021** - Search index optimization with JavaScript Maps

### 2022-2024: Framework Independence
- **2022** - **Major overhaul**: Removed jQuery and underscore.js dependencies (commit 3b01fbe2a)
  - Complete rewrite to vanilla JavaScript
  - Introduced strict mode
  - Used modern ES6+ features (arrow functions, const/let, Sets, Maps)
- **2023** - Performance optimizations and bug fixes
- **2024** - **Latest**: Prettier JavaScript formatting adoption (commit 2c2159fb9)

## Key Feature Additions

### Search Capabilities
1. **Basic text search** (2007)
2. **Object name searching** - `Class.method` style (2008)
3. **Stopword filtering** (2008)
4. **Partial matching** (2013)
5. **Title and subtitle searching** (2017)
6. **Index entry searching** (2018)
7. **Type-dependent results** (2019)

### User Experience
1. **Search result highlighting** (2010)
2. **HTML preview snippets** (2015)
3. **Relevance scoring** (2012, enhanced 2019)
4. **Search summaries** (2017)
5. **Keyboard navigation** (various)
6. **Mobile compatibility** (ongoing)

### Technical Improvements
1. **Asynchronous index loading** (2009)
2. **Search index compression** (2009)
3. **Cross-browser compatibility** (2010-2015)
4. **Performance optimizations** (2019-2021)
5. **Framework independence** (2022)
6. **Modern JavaScript features** (2022-2024)

## Major Architectural Changes

### Dependency Evolution
- **2007-2021**: Heavy reliance on jQuery and underscore.js
- **2022**: Complete removal of external dependencies
- **2024**: Code formatting standardization with Prettier

### Code Structure Changes
- **Early years**: Procedural JavaScript with global functions
- **Mid-period**: Object-oriented approach with Search class
- **Modern era**: ES6+ modules, arrow functions, and modern JavaScript patterns

### Performance Optimizations
- **Index compression**: Grouped objects by prefix, removed redundant data
- **Data structures**: Migrated from arrays to Maps and Sets for better performance
- **Lazy loading**: Asynchronous search index loading
- **Memory efficiency**: Optimized search result storage and retrieval

## Bug Fix Categories

### Search Accuracy (25+ fixes)
- Short word searching
- Exact matching improvements
- Multiple term matching edge cases
- Partial vs full match prioritization

### Browser Compatibility (15+ fixes)
- Internet Explorer support
- WebKit browser fixes
- Chrome-specific issues
- Firefox compatibility

### Performance Issues (10+ fixes)
- Search result display optimization
- Memory usage improvements
- Index loading efficiency

### User Interface (20+ fixes)
- Search result formatting
- Highlighting improvements
- Summary text extraction
- Mobile responsiveness

## Notable Contributors
Based on commit history, key contributors include:
- Georg Brandl (original author)
- Adam Turner (major modernization in 2022-2024)
- Takeshi KOMIYA (numerous bug fixes and improvements)
- Various community contributors

## Current State (2024)
The current searchtools.js is a modern, dependency-free JavaScript module that:
- Uses ES6+ features and modern JavaScript patterns
- Implements comprehensive search with multiple result types
- Provides excellent browser compatibility
- Follows modern code formatting standards
- Maintains backward compatibility with existing Sphinx themes

## Impact and Usage
This file is a critical component of Sphinx's HTML output, powering the search functionality for thousands of documentation sites across the Python ecosystem and beyond. Its evolution reflects the broader trends in web development, from jQuery-heavy code to modern vanilla JavaScript.
