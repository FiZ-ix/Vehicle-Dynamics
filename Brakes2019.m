InchesToMeters = 0.0254;
NewtonMetersSqToPSI = 0.000145038;

wheelbase = 1.59222708; %meters
a = wheelbase / 2;
b = wheelbase / 2;
MassCar = 303.97; %kg
g = 9.81; %m/s^2
WeightVehicle = MassCar * g; %N
StaticRearAxleLoad = WeightVehicle*(a/(a+b));
StaticFrontAxleLoad = WeightVehicle - StaticRearAxleLoad;
TireDiameter = 0.5207; %m
BrakePadCoefficientOfFriction = .3;
RotorOuterRadius = .22/2; %m
RotorInnerRadius = .17555/2; %m
RotorEffectiveRadius = (RotorOuterRadius^3/3-RotorInnerRadius^3/3)/(RotorOuterRadius^2/2-RotorInnerRadius^2/2) ;
AverageCoefficientOfFriction = .75; %Coefficient of Friction Between Tire and Road

BrakingForce = WeightVehicle * AverageCoefficientOfFriction;

HeightCenterofGravity = .2032;

LongitudualLoadTransfer = BrakingForce*HeightCenterofGravity / (a+b);

FrontLeftLoad = (StaticFrontAxleLoad + LongitudualLoadTransfer)/2;
FrontRightLoad = FrontLeftLoad;
RearLeftLoad = (StaticFrontAxleLoad - LongitudualLoadTransfer)/2;
RearRightLoad = RearLeftLoad;

BrakeBias = .8; %Front to Rear
BrakePadCoefficientOfFriction = .3; %Being Conservative Here

FrontLeftBrakingTorque = FrontLeftLoad * AverageCoefficientOfFriction * (TireDiameter/2);
FrontLeftCaliperForce = FrontLeftBrakingTorque / RotorEffectiveRadius;
FrontLeftBrakePadForce = FrontLeftCaliperForce / (2*BrakePadCoefficientOfFriction);

CaliperSlaveCylinderBore = .034 ; %m
CaliperSlaveCylinderArea = 2 * pi * (CaliperSlaveCylinderBore / 2)^2;

FrontBrakePressure = FrontLeftBrakePadForce / CaliperSlaveCylinderArea ;
FrontBrakePressurePSI = FrontBrakePressure * NewtonMetersSqToPSI; 

FrontMasterCylinderBore = .625 * InchesToMeters;
RearMasterCylinderBore = .625 * InchesToMeters; 

FrontMasterCylinderArea = pi * (FrontMasterCylinderBore/2)^2;
RearMasterCylinderArea = pi * (RearMasterCylinderBore/2)^2;

MasterCylinderArea = FrontMasterCylinderArea + RearMasterCylinderArea;

PedalRatio = 4.78;

FootForce = (FrontBrakePressure*MasterCylinderArea)/PedalRatio;



