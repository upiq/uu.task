{ pkgs ? import <nixpkgs> {}
}:


with pkgs.stdenv;

let

  pythonPackages = pkgs.python27Packages;

  inherit (pkgs) fetchurl;
  inherit (pythonPackages) buildPythonPackage;

  check-manifest = buildPythonPackage rec {
    name = "check-manifest-0.25";
    src = fetchurl {
      url = "https://pypi.python.org/packages/source/c/check-manifest/${name}.tar.gz";
      md5 = "119cd42625ee78f9377abeeecd1c95c8";
    };
    buildInputs = with pythonPackages; [ mock pkgs.git pkgs.glibcLocales ];
    preConfigure = ''
      export LANG="en_US.UTF-8"
      export LOCALE_ARCHIVE=${pkgs.glibcLocales}/lib/locale/locale-archive
    '';
  };

  pyroma = buildPythonPackage rec {
    name = "pyroma-1.8.2";
    src = fetchurl {
      url = "https://pypi.python.org/packages/source/p/pyroma/${name}.tar.gz";
      md5 = "7490b824c1bf3713660746f06ed1c68b";
    };
    propagatedBuildInputs = with pythonPackages; [ docutils ];
  };

  # TODO
  # buildoutCache = import ./buildout-cache.nix { inherit (pkgs) fetchurl fetchzip; };

in mkDerivation{
  name = "uu.task";

  src = builtins.filterSource (path: type:
          builtins.elem (baseNameOf path) (
            builtins.filter (x: ! (builtins.elem x [
                "doc" "uu" "buildout.cfg" "CHANGES.rst" "Makefile" "MANIFEST.in"
                "README.rst" "screenshot2.png" "screenshot.png" "setup.py" ]))
              (builtins.attrNames (builtins.readDir ./.))
          )) ./.;

  buildInputs = with pythonPackages; [
    pkgs.libxml2
    pkgs.libxslt
    pkgs.git
    pkgs.nodejs
    zc_buildout2
    flake8
    check-manifest
    pyroma
  ] ++ (builtins.attrValues pythonPackages.python.modules);

  checkPhase = ''
    make test
  '';

  buildPhase = ''
    # TODO:
    # buildout -o buildout.cfg
  '';

}
