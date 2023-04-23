{ config, lib, pkgs, ... }: let
  bing-gpt-server = pkgs.callPackage ./default.nix { };
  cfg = config.services.bing-gpt-server;
in {

  options = {
    services.bing-gpt-server = {
      enable = lib.mkEnableOption "Bing GPT Server";
      cookieFile = lib.mkOption {
        type = lib.types.path;
        description = "Path to the cookie file.";
      };
      address = lib.mkOption {
        type = lib.types.str;
        default = "localhost";
        description = "Address to listen on.";
      };
      port = lib.mkOption {
        type = lib.types.port;
        default = 8000;
        description = "Port to listen on.";
      };
    };
  };
  config = lib.mkIf config.services.bing-gpt-server.enable {
    systemd.services.bing-gpt-server = {
      description = "Bing GPT Server";
      wantedBy = [ "multi-user.target" ];
      environment = {
        COOKIE_PATH = "%d/bing-gpt-cookie-file";
        PORT = "${toString cfg.port}";
        PYTHONPATH = "${pkgs.python3.pkgs.makePythonPath [ bing-gpt-server ]}";
      };
      serviceConfig = {
        LoadCredential = "bing-gpt-cookie-file:${cfg.cookieFile}";
        ExecStart = "${pkgs.python3Packages.hypercorn}/bin/hypercorn --bind ${cfg.address}:${toString cfg.port} bing_gpt_server:app";

        StateDirectory = "bing-gpt-server";
        WorkingDirectory = "bing-gpt-server";

        Restart = "always";
        User = "bing-gpt-server";
        Group = "bing-gpt-server";
        DynamicUser = true;
        RestartSec = 5;
      };
    };
  };
}
