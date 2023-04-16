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
    };
  };
  config = lib.mkIf config.services.bing-gpt-server.enable {
    systemd.services.bing-gpt-server = {
      description = "Bing GPT Server";
      wantedBy = [ "multi-user.target" ];
      serviceConfig = {
        Environment = "COOKIE_FILE=%d/bing-gpt-cookie-file";
        LoadCredential = "bing-gpt-cookie-file:${cfg.cookieFile}";
        ExecStart = "${bing-gpt-server}/bin/bing-gpt-server";
        Restart = "always";
        User = "bing-gpt-server";
        Group = "bing-gpt-server";
        DynamicUser = true;
        RestartSec = 5;
      };
    };
  };
}
