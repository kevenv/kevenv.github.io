# CSS cheatsheet

## HTML
- HTML (Hyper Text Markup Language)
- content of the web
- home = `index.html`
- defined by a hierarchy of tags: `<element>content</element>`

Basic HTML page:
```HTML
<!DOCTYPE html>
<html lang="en">
	<head>
        <meta charset="utf-8">
		<title>My website</title>
	</head>
	<body>
		<h1>My website</h1>
		<p>Hello world!</p>
	</body>
</html>
```

### Elements
- can have attributes `<element attr=""></element>`
    - some are required
    - some are optional

- heading: `<h1>, <h2>, <h3>, <h4>, <h5>, <h6>`
    - only one `<h1>` per page
- paragraph: `<p>`
- important: `strong`
- emphasis: `em`
- link: `<a>`
```HTML
<a href="https://www.website.com">website</a>
```


### Lists
- `<ol>` : ordered / numbered 
- `<ul>` : unordered / bullets 

```HTML
<ul>
    <li>item 1</li>
    <li>item 2</li>
    <li>item 3</li>
</ul>
```

### Images
```HTML
<img src="file_path.jpg" alt="">
```

- `alt` (required)
    - description, intent of image
    - no need to say "an image of ..."
    - "" if decorative image

### Layout elements
- `<div>` : generic block element
- `<span>` : generic inline element
- `<header>` : header
- `<footer>` : footer
- `<nav>` : menu
- `<main>` : main content
- `<section>` : section of content

### Types of element
- inline : in a paragraph, no new line
- block : out of paragraphs, new line

### Paths
- `href`, `src` attributes
- absolute path (external) : `https://website.com/page.html`
- relative path (local) : `directory/page.html`

### Comments
```HTML
<!-- comment -->

<!-- very very 
long comment -->
```

## CSS
- CSS (Cascading Style Sheet)
- style/look of the web
- defined as a list of rule with `property: value;`

### 3 ways to use

#### Inline CSS
- only used for JS scripts
- via the `style` attribute
```HTML
<p style="property: value; property: value">my paragraph</p>
```

#### Internal CSS
```HTML
<head>
    <style>
        element { /* rule */
            property: value; /* declaration */
            property: value;
        }
    </style>
</head>
```

#### External CSS
- like `#include`

```HTML
<head>
    <link href="style.css" rel="stylesheet">
</head>
```

### Selectors
- element
```CSS
element {

}
```

- class
```HTML
<p class="my-class"></p>
```

```CSS
.my-class {

}

/* or */

element.my-class {

}
```

- id
    - can only be used once per page
    - has priority over class
    - don't use unless JS, anchors..

```HTML
<p class="my-id"></p>
```

```CSS
#my-id {

}
```

### Properties
- `font-size`
- `color` : text color
- `background-color`
- `text-align` : left, center, right

### Colors
```CSS
p {
    color: red;
    color: #FF00FF; /* RRGGBB */
    color: #F0F; /* RGB */
    color: rgb(255, 0, 255);
    color: hsl(100, 100%, 75%);
}
```

### Size units
- px
    - absolute
    - doesn't scale/responsive
- %
    - relative to parent
- em
    - relative to current/parent `font-size`
    - good for padding/margin
- rem (root-em)
    - relative to root/html `font-size`
    - good for `font-size`
- vh
    - relative to the height of the viewport
    - 1vh = 1% viewport height
- 0 (no units)
- auto

### Comments
```CSS
/* comment */
```

### Mobile
```HTML
<meta name="viewport" content="width=device-width, initial-scale=1">
```

### Center elements horizontally
```CSS
.my-class {
    /* align to the right */
	margin-left: auto /* fill left with empty space */
	
	/* align to center */
	width: 100px

	margin-left: auto
	margin-right: auto
		/* or */
	margin: 0 auto /* preferred way */
		/* or */
	margin: auto
}
```

### Flexbox
```HTML
<div class="container">
    <div class="item">1</div>
    <div class="item">2</div>
    <div class="item">3</div>
</div>
```

```CSS
.container {
    display: flex;
}
```

- `justify-content` (x axis)
	- flex-start
	- flex-end
	- center
	- space-between : equal spacing between items
	- space-around : equal spacing around items
	- space-evenly : items evenly spaced in container
- `align-items` (y axis)
	- stretch : resized to fit container
	- flex-start
	- flex-end
	- center
	- baseline : align to each item contents
- `flex-direction`
	- row
	- row-reverse
	- column
	- column-reverse
- `order` : specifies the order of a flexible item (-2,-1,0,1,2)
- `align-self` : "align-items" for a single item
- `flex-wrap` : when items doesn't fit into container, used with "align-content"
	- nowrap
	- wrap
	- wrap-reverse
- `flex-flow` : "flex-direction" + "flex-wrap"
- `align-content` : spacing between lines
	- stretch
	- flex-start
	- flex-end
	- center
	- space-between
	- space-around
- `gap` : row-gap column gap
- `row-gap` : spacing between rows
- `column-gap` : spacing between columns

### Debug tricks
```CSS
* {
    border: 2px solid red; /* show all boxes */
}
```
