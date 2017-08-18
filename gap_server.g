# LogTo(); # to close log file if it was opened from .gaprc
LoadPackage("scscp");
LoadPackage("factint");

SCSCPserviceName:="GAP-SCSCP-demo-group-numbers";

SCSCPserviceVersion:= Concatenation(
        "GAP ", GAPInfo.Version,
        "; CubeFree ", GAPInfo.PackagesInfo.cubefree[1].Version,
        "; Gnu ", "https://github.com/alex-konovalov/gnu",
        "; GrpConst ", GAPInfo.PackagesInfo.grpconst[1].Version,
        "; SCSCP ", GAPInfo.PackagesInfo.scscp[1].Version,
        "; SglPPow ", GAPInfo.PackagesInfo.sglppow[1].Version );

SCSCPserviceDescription:= 
  "GAP SCSCP demo server with numbers of isomorphism types of finite groups. Server started";

InstallSCSCPprocedure("orbit",
  function()
    Print("yo");
    return 0;
  end
 );

RunSCSCPserver( SCSCPserverAddress, 26134);
