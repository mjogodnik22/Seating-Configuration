=====SEATING CONFIGURATION TOOL=====  
This tool was created by Matt Jogodnik under the guidance of Anthony Volpe  
while working at Quantworks. Its intent is to organize seating blocks  
to maximize profit for vendors while at the same time prioritizing safety  
for clientele.  

**V1:** IO added (txt format), basic processing based on cubes of 16 seats only  
and an *m* x *n* seating rectangle - completed 7/3/20

**V2:** Expanded to allow seating blocks in the form of a *p* x *q* rectangle  
s.t. *p* x *q*=12 - completed 7/6/20

**V3:** Removed vertical line seating configurations, created search at end  
to check if 2, 4, or 8 seat blocks can be squeezed in - completed 7/6/20

**V4:** Added a diagonal parameter for spacing as well as parametized x and y  
spacing. Allowed for different-sized blocks. Created goodness score KPI that
balances seating efficiency (which is maximized by large seating blocks) with  
an availability of more marketable small seating blocks - completed 7/10/20  
- [X] Diagonal parameter and parametized x,y spacing - completed 7/9/20
- [X] Allow for different-size blocks - completed 7/10/20
- [X] Create goodness score KPI - completed 7/10/20

**V5:** Came up with some convergence data on the upper bound of g, the  
goodness score. Improved commenting within functions, especially those
that would be confusing to follow with a pre-commenting scheme alone.  
Added goodness score calculations to separate function to allow
for parametization of weighting - IP
- [X] Convergence data and automated time-keeping - completed 7/13/20
- [X] Improved/overhauled commenting - completed 7/13/20
- [X] Separated goodness score function - completed 7/12/20

**V6:** Added support for stadiums with multiple *m* x *n* sections - completed  
7/21/20
- [] Added support for seating chart file format as input - postponed for now
- [X] Added support for stadiums with multiple sections - completed 7/21/20

**V7:** Updated goodness score for overall seating to remain comparable with  
section seating - completed 7/24/20

**V8:** The Big Update: Updated to accept any quadrilateral or triangle as input  
(not just an *m* x *n* rectangle). Updated to allow the use of any shape as a  
seating block (not just a *p* x *q* rectangle). Changed algorithm to prioritize  
placement of larger seating blocks in obtuse angles and smaller seating blocks  
in acute angles. Started allowing user-entered buffer seats along aisle - IP  
- [X] Removed rectangular constraint for seating maps - completed 7/28/20
- [] Removed rectangular constraint for seating blocks
- [] Updated algorithm based on angles
- [X] Added seating aisle buffer - completed 7/29/20 