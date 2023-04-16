{ pkgs ? import <nixpkgs> {} }:
let
  pythonPkgs = pkgs.python3.pkgs;
in
pythonPkgs.buildPythonApplication {
  name = "bing-gpt-server";
  src =  ./.;
  propagatedBuildInputs = with pkgs; [
    pythonPkgs.quart
    (pythonPkgs.callPackage ./edge-gpt { })
  ];
  meta = {
    description = "A simple HTTP server for the Edge-GPT";
    homepage = "https://github.com/Mic92/bing-gpt-server";
  };
}
