# Project
鑽徑補償

# Project Goal
1.半自動化將所有通孔/盲孔/埋孔從成品徑補償為鑽徑。

# Release Log
1. 2023/04/14 測試上線
2. 2023/05/10 加入九個pad?
3. 2023/08/03 第三條測試內容

# Dev Log
1. 2023/03/15 ezcam first version
2. 2023/03/20 genesis/ incam version
3. 2023/03/24 update slot to be done version in genesis/ Incam
4. 2023/04/07 genesis teseted version
5. 2023/04/12 incam tested version and update some function, genesis untested
6. 2023/05/10 fix NVOP no drill bug, module text name, change 3 cps calculate methods, slot float issue, add pause button.
7. 2023/05/24 (patrick)update slot editor, modify finish size/tol+/ tol- in one widget 
8. 2023/05/24 (patrick)hidden vop column/ call drill_calculate when total_thickness/cu_thickness changed
9. 2023/05/24 (patrick)add drill size data when calling drill_calculate
10. 2023/05/24 (patrick)only check current layer format in second modify mode
11. 2023/05/24 (patrick)lock Dcode/Number column
12. 2023/06/05 (patrick)only etl cuurent layer to backend in second modify mode
13. 2023/06/09 (Darcy)non_plated_cps, return higher srill size when there's two drills that have same distance
14. 2023/06/09 (Darcy)plated_cps, when fszie > 256, return +4/+6 drill value 
15. 2023/06/09 (Darcy)NVOP_CPS should consider user's input drill value
16. 2023/06/09 (Darcy)add VIP tols info after change its drill type (label, label judging, foolproof)
17. 2023/07/12 (Darcy).drl add blind hole logic ex:blind-d2-10 >>get_gerber_drl_dict
18. 2023/07/17 (Darcy) TCODE re string change from int to string
19. 2023/07/27 (Darcy) Fix via not finding correct drill and tols
20. 2023/07/27 (Darcy) Fix via not judge correctly
21. 2023/08/01 (Darcy) slot tols can not be read when num > 1
22. 2023/08/14 (Darcy) incam qctx gerber slot forgot to add is_slot info solved
23. 2023/08/14 pth slot compensation doesn't apply to relay hole logic, come with normal pth logic
# Reference