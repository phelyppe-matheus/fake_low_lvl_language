<style type="text/css">
    pre.code {
        white-space: pre-wrap;
    }
    pre.code::before {
        counter-reset: listing;
    }
    pre.code code {
        counter-increment: listing;
    }
    pre.code code:empty::after {
        content: '[...]';
        counter-increment: listing 10;
    }
    pre.code code::before {
        content: counter(listing) ". ";
        display: inline-block;
        width: 4em;
        padding-left: auto;
        margin-left: auto;
        text-align: right;
    }
</style>

# Fake Low Level Language for Computer Architecture classes


## Usage example
```
python main.py example\bublesort
```

`Warning: For better use try to use it on a fullscreen terminal.`


## Common structures on Linguagem Muito Simples
### FOR / WHILE
<pre class='code'>
<code>// int i;</code>
<code>// i = 1;</code>
<code>// while(1<5){</code>
<code>//      i=i+1;</code>
<code>// }</code>
<code></code>
<code>// choose and set the variable's location yourself</code>
<code>// here we will use memory 10</code>
<code></code>
<code>load 0 </code> // value at memory[0] is always 0
<code>addi 1 </code> // 1
<code>store 10 </code> // i=1
<code>    load 10 </code> // gets i
<code>    subi 4 </code> // asks i&#x3e;5
<code>    jpos 51 </code> // if false go to end
<code></code>
<code>    load 10 </code> // gets i
<code>    addi 1 </code> // i+1
<code>    store 10 </code> // i=i+1
<code>    jump 33</code>  // always go to the loop's beggining
<code></code> // 'loop_end'
</pre>