// SPDX-License-Identifier: UNLICENSED
pragma solidity >=0.7.0 <0.9.0;

contract MockContract {
    bool public myvar = false;

    constructor(bool _myvar) {
        myvar = _myvar;
    }
}
