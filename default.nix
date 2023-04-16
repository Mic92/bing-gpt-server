{ pkgs ? import <nixpkgs> {} }:
let
  pythonPkgs = pkgs.python3.pkgs;
in
pythonPkgs.buildPythonPackage {
  name = "bing-gpt-server";
  src =  ./.;
  propagatedBuildInputs = [
    pythonPkgs.quart
    (pythonPkgs.callPackage ./edge-gpt { })
  ];
  meta = {
    description = "A simple HTTP server for the Edge-GPT";
    homepage = "https://github.com/Mic92/bing-gpt-server";
  };
}
