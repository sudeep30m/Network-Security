var subst = require('./substitution/substitution_box.js');
var shiftRow = require('./shift_row.js');
var mixColumn = require('./mix_column.js');
var keyGenerator = require('./key_expansion.js');

// Simply xor of Input and key matrix
function addRoundKey(a, b) {
    var n = a.length;
    var m = a[0].length;
    for (let i = 0; i < n; i++) {
        for (let j = 0; j < m; j++)
            a[i][j] = a[i][j] ^ b[i][j];
    }
    return a;
}

// Input 4 * 4 matrix each entry a 8-bit binary string 
// Output 4 * 4 matrix each entry a decimal number from 0 to 255
function binToNumMatrix(input){
    return input.map(function (x) {
            x = x.map(x => parseInt(x, 2));
            return x;
        });
    }    

// input = 128  bit hex string output = 128 bit hex string
function aesEncryption(input, key) {
    console.log("Input = %s\n", input);
    input = keyGenerator.hexToBinaryString(input);
    input = keyGenerator.stringToBinMatrix(input);
    input = binToNumMatrix(input);
    var keyMatrix = keyGenerator.keyMatrix(key, 0);
    input = addRoundKey(input, keyMatrix);
    console.log("After Round 0 of encryption: %s", keyGenerator.matrixToString(input) );
        
    for (let round = 1; round <= 10; round++) {
        input = subst.substitution(input);
        // console.log("After Substitution",input,"\n");
        input = shiftRow.shiftRow(input);
        // console.log("After Shift Row",input,"\n");
        if (round != 10)
            input = mixColumn.mixColumn(input);
        //console.log("After mix column", input, "\n");
        keyMatrix = keyGenerator.keyMatrix(key, round);
        // console.log(keyMatrix);
        input = addRoundKey(input, keyMatrix);
        console.log("After Round %d of encryption: %s", round, keyGenerator.matrixToString(input) );
        //console.log();
    }
    return keyGenerator.matrixToString(input);
}

// input = 128  bit hex string output = 128 bit hex string
function aesDecryption(input, key) {
    console.log("Cipher text = %s", input);
    input = keyGenerator.hexToBinaryString(input);
    input = keyGenerator.stringToBinMatrix(input);
    input = binToNumMatrix(input);
    var keyMatrix = keyGenerator.keyMatrix(key, 10);
    input = addRoundKey(input, keyMatrix);
    // console.log("After Round 0 of decryption: %s", keyGenerator.matrixToString(input) );
    for (let round = 1; round <= 10; round++) {
        input = shiftRow.inverseShiftRow(input);
        // console.log("After inverse shift row", input, "\n");
        input = subst.inverseSubstitution(input);
        console.log("After Round %d of decryption: %s", round  - 1, keyGenerator.matrixToString(input) );
        keyMatrix = keyGenerator.keyMatrix(key, 10 - round);
        input = addRoundKey(input, keyMatrix);
        if(round == 10)
            console.log("After Round %d of decryption: %s", round, keyGenerator.matrixToString(input) );
        if (round != 10)
            input = mixColumn.inverseMixColumn(input);
        // console.log("after mix column", input, "\n");
    }
    return keyGenerator.matrixToString(input);
}


var key = "0abcdef1234567890abcdef123456789";
var input = "0abc12f1a34567890abcdef123422788";
var cipher = (aesEncryption(input, key));
console.log("\n---------------------------------\n");
aesDecryption(cipher, key);
