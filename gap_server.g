# LogTo(); # to close log file if it was opened from .gaprc
LoadPackage("scscp");
LoadPackage("factint");

SCSCPserviceName:="GAP-SCSCP-demo-group-numbers";
OMsymRecord.ring3.integers := Integers;

SetInfoLevel(InfoSCSCP, 10);

SCSCPserviceVersion:= Concatenation(
        "GAP ", GAPInfo.Version,
        "; CubeFree ", GAPInfo.PackagesInfo.cubefree[1].Version,
        "; Gnu ", "https://github.com/alex-konovalov/gnu",
        "; GrpConst ", GAPInfo.PackagesInfo.grpconst[1].Version,
        "; SCSCP ", GAPInfo.PackagesInfo.scscp[1].Version,
        "; SglPPow ", GAPInfo.PackagesInfo.sglppow[1].Version );

SCSCPserviceDescription:= 
  "GAP SCSCP demo server with numbers of isomorphism types of finite groups. Server started";

InstallSCSCPprocedure("orbit_of_list", 
  function(group, list)
    local orbit, perm, variation, i;
    orbit := [];
    for perm in Set(group) do
      variation := [];
      for i in [1..Length(list)] do
        Add(variation, list[i^perm]);
      od;
      Add(orbit, variation);
    od;
    return orbit;
  end
);

R := PolynomialRing(Integers, 4);
SetOpenMathDefaultPolynomialRing(R);

OnMultivariatePolynomialsVariables := function(poly, perm)
       local i, j, extrep, fam;

       fam := FamilyObj(poly);
       extrep := MutableCopyMat(ExtRepPolynomialRatFun(poly));
       for i in [1,3..Length(extrep)-1] do
               for j in [1,3..Length(extrep[i])-1] do
                       extrep[i][j] := extrep[i][j]^perm;
               od;
       od;    

       return PolynomialByExtRep(fam, extrep);
end;

OMsymRecord.gap1 := rec( OnMultivariatePolynomialsVariables := OnMultivariatePolynomialsVariables );

InstallSCSCPprocedure("SymmetricGroup", SymmetricGroup);
InstallSCSCPprocedure("DihedralGroup", DihedralGroup);
InstallSCSCPprocedure("Orbit", Orbit);
# InstallSCSCPprocedure( "GetGAPVariable", name -> ValueGlobal(name), "refer to a global GAP object", 1, 1 );

RunSCSCPserver( SCSCPserverAddress, 26134);
