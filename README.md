# Fake Low Level Language for Computer Architecture classes


## Usage example
```
python main.py example\bublesort
```

`Warning: For better use try to use it on a fullscreen terminal.`


## Common structures on Linguagem Muito Simples
### FOR / WHILE
```javascript
// int i;
// i = 1;
// while(1<5){
//     [...]
//     i=i+1;
// }

// choose and set the variable's location yourself
// here we will use memory 10

load 0 // value at memory[0] is always 0
addi 1 // 1
store 10 // i=1
    load 10 // 'loop_begin' gets i
    subi 4 // asks i<5
    jpos 'loop_end' // if false go to end
    [...]
    load 10 // gets i
    addi 1 // i+1
    store 10 // i=i+1
    jump 'loop_begin' // always go to the loop's beggining
[...] // 'loop_end'
```

### DO WHILE
```javascript
// int i;
// i = 1;
// do{
//     [...]
//     i=i+1;
// }while(i<5);

// choose and set the variable's location yourself
// here we will use memory 10

load 0 // value at memory[0] is always 0
addi 1 // 1
store 10 // i=1
    [...] // 'loop_begin'
    load 10 // gets i
    addi 1 // i+1
    store 10 // i=i+1
    subi 4 // asks i<5
    jpos 'loop_end' // if false go to end
    jump 'loop_begin' // always go to the loop's beggining
[...] // 'loop_end'
```
