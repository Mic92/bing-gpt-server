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

  doCheck = false; # fixme httpx tries to resolve host

  postBuild = ''
    export COOKIE_PATH=cookies.json
    echo "[]" > cookies.json
  '';
  meta = {
    description = "A simple HTTP server for the Edge-GPT";
    homepage = "https://github.com/Mic92/bing-gpt-server";
  };
}
