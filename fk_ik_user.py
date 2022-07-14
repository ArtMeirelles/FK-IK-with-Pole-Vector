import maya.cmds as cmds

# General Vars
name_user="JointsName"
NewJointName = 'JointsN'
loc_list=[]
the_joint=[]
i=[]
to_rename = []
first_run = True
in_joint_made = False
out_joint_made = False
window_maker = []
updated_index = 0
main_grp = []
wheel_ctrl = []
world_ctrl = []

    ### Auto Rig Functions ###
    
    # Make Locators
def locator_pivot():
    posX = posY = posZ = 0
    selection = cmds.ls(sl=True, fl=True)

    # Condition for if nothing is selected
    try:
        obj = cmds.ls(sl=True)[0]

    except IndexError:
        cmds.error("No object or vertices selected")

    # Stores all vertices in a list if a mesh is selected
    vert_selection = cmds.ls(obj + ".vtx[*]", fl=True)

    # Stores all vertices in a list if individual vertices are selected instead of a mesh
    for i in cmds.ls(sl=True, fl=True):
        if ".vtx" in i:
            vert_selection = selection
            break

    # Adds up all the 'X', 'Y', and 'Z' positions of all selected vertices
    for i in vert_selection:
        position = cmds.xform( i, q=True, translation=True, ws=True )
        posX+=position[0]
        posY+=position[1]
        posZ+=position[2]

    position[0] = posX/len(vert_selection)
    position[1] = posY/len(vert_selection)
    position[2] = posZ/len(vert_selection)

    # Creates a locator and moves it to the average position of all vertices selected
    cmds.move(position[0], position[1], position[2], cmds.spaceLocator(n='_Jnt1'))
    locs = cmds.select('_Jnt*')
    loc_list = cmds.ls(sl=True,type='transform')
    print (loc_list)
    cmds.select(cl=True)

    # Undo Locators
def delete_locators():
    global loc_list
    cmds.select(loc_list)
    loc_list=[]
    cmds.select(cl=True)
    if cmds.objExists('_Jnt*')!=True:
        pass
    else:
        #cmds.select(all=True)
        loc_lis = cmds.ls(sl=True, type='transform')
        loc_d = cmds.select('_Jnt*')
        cmds.delete()
          
    # Functions to create joints where the locators are placed
def make_joints():
        if cmds.objExists('_Jnt*')!=True:
            cmds.warning('Please, first create the locators')
        else:
            locs = cmds.select('_Jnt*')
            loc_list = cmds.ls(sl=True,type='transform')
            print (loc_list)
            cmds.select(cl=True)
            for i in loc_list:
                the_joint = cmds.joint(n=name_user + '%s' %i + '_skin', rotationOrder = "xyz")
                print (the_joint)
                sel = cmds.ls(sl=True, type='joint')
                cmds.select(sel)
                print (sel)
                Thelocator=i
                cmds.matchTransform(the_joint,Thelocator,pos=True)
            else:
                cmds.select(cl=True)

    # Show Axis for Joints
def show_axis_display(display=True):
    cmds.listRelatives(allDescendents=True, type='joint')
    cmds.select(hi=True,add=True)
    cmds.ls(sl=True,type='joint')
    if len(cmds.ls(sl=1, type="joint")) == 0: # if no joints are selected, do it for all the joints in the scene
        jointList = cmds.ls(type="joint")
    else:
        jointList = cmds.ls(sl=1, type="joint")
    for jnt in jointList:
        cmds.setAttr(jnt + ".displayLocalAxis", display) # set the displayLocalAxis attribute to what the user specifies.

    # Hide Axis for Joints
def hide_axis_display(display=False):
    cmds.listRelatives(allDescendents=True, type='joint')
    cmds.select(hi=True,add=True)
    cmds.ls(sl=True,type='joint')
    if len(cmds.ls(sl=1, type="joint")) == 0: # if no joints are selected, do it for all the joints in the scene
        jointList = cmds.ls(type="joint")
    else:
        jointList = cmds.ls(sl=1, type="joint")
    for jnt in jointList:
        cmds.setAttr(jnt + ".displayLocalAxis", display) # set the displayLocalAxis attribute to what the user specifies.
   
def ik_maker():
    cmds.ls(sl=True,type='joint')
    if len(cmds.ls(sl=1, type="joint")) == 0:  # Make sure that user select the root joints
        cmds.warning('Please, first select the root joint!')
    else:
        IKSelec = actObject
        print (IKSelec)
        last_jnt = ik_selc
        print (last_jnt)
        rp_IK = cmds.ikHandle( sol='ikRPsolver', sj=(IKSelec), ee=(last_jnt))

    
    
def hierarchy_func():
    children_joints = cmds.listRelatives(allDescendents=True, type='joint')
    cmds.select(children_joints, add=True)
   
def box_curve_ctrl():
    cmds.curve(n='Box_CTRL', d=1, p=[(1,-1,1), (-1,-1,1),
    (-1,-1,-1), (1,-1,-1),
    (1,-1,1), (1,1,1), (-1,1,1),
    (-1,-1,1), (-1,1,1), (-1,1,-1),
    (-1,-1,-1), (-1,1,-1), (1,1,-1),
    (1,-1,-1), (1,1,-1), (1,1,1)]
    )

def resize():
    items = cmds.ls(sl=True,type='transform')
    for item in items:
        cmds.select(item + '.cv[0:*]', r=True) # selecting all(*) the curve vertex(.cv)
        cl = cmds.cluster()
        cl_resize = cmds.rename(cl[1],item + '_resize') # renaming just the clusterHandle, because just him is needed to scale the curve
        cmds.addAttr(item, ln='radius', at='double', min=0, dv=1)
        cmds.setAttr(item + '.radius', e=True, k=False, channelBox=True)
        rad = item + '.radius'
        cmds.connectAttr(rad,cl_resize + '.sx', f=True)
        cmds.connectAttr(rad,cl_resize + '.sy', f=True)
        cmds.connectAttr(rad,cl_resize + '.sz', f=True)
        cmds.setAttr(cl_resize + '.visibility', 0)
        cmds.select(cl=True)
            
def grouping():
    sel = cmds.ls(sl=True,type='transform')
    for each in sel:
        offset_f = cmds.group(n=each + '_offset', em=True)
        world  = cmds.group(n=each + '_grp') # the world group is not empty because the offset group will be parent to him
        cmds.delete(cmds.parentConstraint(each, world)) # align the world group
        getParents=cmds.listRelatives(each, p=True)
        if getParents: # making sure that the hierarchy was repect
            cmds.parent(world, getParents[0])
        cmds.parent(each)
        
def select_world_ctrl():
    cmds.select(cl=True)
    cmds.select(all=True)
    sel_world_ctrl = cmds.ls(sl=True, type="transform")
    cmds.select('world_ctrl')

        
def fk_rg():
        jnts = cmds.ls(sl=True, type= 'joint')
        print (jnts)
        for i in range(len(jnts)):
            box_curve_ctrl()
            ctrl_node = cmds.ls(sl=True,type='transform')[0] # because the 'box_curve_ctrl' is a 'trasnform type'
            cmds.delete(cmds.parentConstraint(jnts[i], ctrl_node)) # Align translation and rotation using parent contraint and deleting
            jnt_id = jnts[i].split('_skin')# split is like before the "line" is zero and after is 1
            print (jnt_id[0]) # find anything before the "split"
            ctrl = cmds.rename(ctrl_node, jnt_id[0] + '_CTRL') # Rename "box ctrl"
            cmds.select(ctrl, r=True) # force the selection of the control(ctrl)
            #order_joints()
            resize() # make sure to resize the controls
            cmds.select(ctrl, r=True) # making sure the cluster will be selected
            grouping()
            cmds.parentConstraint(ctrl, jnts[i]) # constraint the joints to the controls
            cmds.connectAttr(ctrl + '.scale', jnts[i] + '.scale', f=True) # drive the joint scale and force connection
            axis_xyz = ['x','y','z']
            for axis in axis_xyz:
                cmds.setAttr(ctrl + '.s' + axis, e=True, l=True, k=False) # lock the scale channels
            cmds.setAttr(ctrl + '.visibility', e=True, l=True, k=False) # disable visibility
            cmds.addAttr(ctrl,ln='parent', min=0, max=1, dv=1) # Here we start the dynamic parenting
            cmds.setAttr(ctrl + '.parent', e=True, k=True) # make sure that the parent attribute appears on the control
        cmds.select(cl=True ) # make sure to clear the selection (so we are able to 'tgl' all the controls)
        for each in jnts:
            jnt_id = each.split('_skin')[0] # assign prefix to jnt_id
            cmds.select(jnt_id + '_CTRL', tgl=True ) # select FK controls
        crvs = cmds.ls(sl=True, type='transform') # store selection of the controls in a VAR
        print (crvs)
        for x in range(1,len(crvs)): # be sure that the first object will be the parent object and the second will get constraint
            cmds.parentConstraint(crvs[x-1], (crvs[x] +  '_grp'), mo=True) # 'x' represent the second object and '_grp' it's the world group
            cmds.setKeyframe((crvs[x] +  '_grp'), at=['translate','rotate']) # keyframe translation and rotation
            cmds.connectAttr(crvs[x] + '.parent', (crvs[x] +  '_grp.blendParent1'), f=True) # connect the blend parent to the parent attribute



def ik_rg():
    objs = cmds.ls(sl=True, type= 'transform') # store transform selection in 'objs' and apply this control to a transform type
    print (objs)
    for obj in objs:
        box_curve_ctrl()
        ctrl_node = cmds.ls(sl=True,type='transform')[0] # because the 'box_curve_ctrl' is a 'trasnform type'
        print (ctrl_node)
        parent_ctrl = cmds.delete(cmds.parentConstraint(obj, ctrl_node)) # Align translation and rotation using parent contraint and deleting
        print (parent_ctrl)
        jnt_id = obj.split('_skin')# split is like before the "line" is zero and after is 1
        print (jnt_id[0]) # find anything before the "split"
        ctrl = cmds.rename(ctrl_node, jnt_id[0] + '_ik_CTRL') # Rename "box ctrl"
        print (ctrl)
        selc_ctrl = cmds.select(ctrl, r=True) # force the selection of the control(ctrl)
        print (selc_ctrl)
        #order_joints()
        resize() # make sure to resize the controls
        cluster = cmds.select(ctrl, r=True) # making sure the cluster will be selected
        print (cluster)
        grouping()
        parents = cmds.parent(obj)
        print (parents)
        xyz = ['sx','sy','sz','visibility']
        for ctrls in ctrl:
            for axis in xyz:
                    cmds.setAttr(ctrl + '.' + axis, edit=True, lock=True, keyable=False)
            
    # Resize function in nurbs channels
def resize_circle():
    objs = cmds.ls(selection=True, type='transform')
    for obj in objs:
        cmds.addAttr(obj, longName='radius', attributeType='double', min=0, defaultValue=1)
        cmds.setAttr(obj + '.radius', edit=True, keyable=False, channelBox=True)
        cmds.connectAttr((obj + '.radius'), (obj + '_attrs.radius'), force=True) # connecting radius channel from the input to the displayable channel
         
    # Lock channels and making sure they are not keyable
def lock_xform_channel():
    objs = cmds.ls(selection=True, type='transform')
    trs = ['t','r','s']
    xyz = ['x','y','z']
    for obj in objs:
        for attr_trs in trs:
            for axis in xyz:
                cmds.setAttr(obj + '.'+ attr_trs + axis, edit=True, lock=True, keyable=False)
            
def string_replace(string, search, replace):
    if string == '':
        return ''
    replace_string = string.replace(search, replace)
    return replace_string
            
def get_short_name(obj):
    if obj == '':
        return ''
    split_path = obj.split('|')
    if len(split_path) >= 1:
        short_name = split_path[len(split_path)-1]
    return short_name
            
def rename_search_replace(obj_list, search, replace):
    for obj in obj_list:
        object_short_name = get_short_name(obj)
        new_name = string_replace(str(object_short_name), search, replace)
        if cmds.objExists(obj) and 'shape' not in cmds.nodeType(obj, inherited=True) and obj != new_name:
            to_rename.append([obj,new_name])
            
    for pair in reversed(to_rename):
        if cmds.objExists(pair[0]):
            cmds.rename(pair[0], pair[1])
     

    #Tread Functions
def make_locator():
    global first_run
    make_locator.front_locator = cmds.spaceLocator(n = "CircleLocator_Front")
    cmds.scale(3,3,3)
    cmds.move(0,0,10, r = True)
    make_locator.back_locator = cmds.spaceLocator(n = "CircleLocator_Back")
    cmds.scale(3,3,3)
    
    #Only prompt for locator placement the first time the user runs the program
    if first_run == True:
        cmds.confirmDialog(title = "Locator Placement", message = "Place the Locators where you need.")
        first_run =  False
    cmds.button(window_maker.init_button, edit = True, enable = False)
    cmds.button(window_maker.reset_button, edit = True, enable = True)
    cmds.button(window_maker.curve_button, edit = True, visible = True, enable = True)

def reset_locator():
    #Delete Locators
    cmds.delete(make_locator.front_locator)
    cmds.delete(make_locator.back_locator)
    
    #Hide Buttons
    cmds.button(window_maker.init_button, edit = True, enable = True)
    cmds.button(window_maker.curve_button, edit = True, enable = False, visible = False)
    cmds.button(window_maker.reset_button, edit = True, enable = False)
    cmds.textFieldButtonGrp(window_maker.text_button, edit = True, enable = False, visible = False, text = "")
    cmds.intSliderGrp(window_maker.copies_slider, edit= True, visible= False, value=0)
    cmds.text(window_maker.text_tread, edit=True, visible=False)
    
    # If the user resets before the Curve gets created, just try to get it and ignore the Error
    try:
        cmds.delete(make_curve.tread_curve)
        cmds.delete(make_curve.locator_group)
        cmds.delete(numchange.new_polyobject)
    except AttributeError:
        pass
    except ValueError:
        pass
        
def make_curve():
    cmds.select(make_locator.front_locator)
    front_locator_position = cmds.getAttr(".translateZ")
    cmds.select(make_locator.back_locator)
    back_locator_position = cmds.getAttr(".translateZ")
    print(front_locator_position)
    print(back_locator_position)
    locator_distance = abs(front_locator_position-back_locator_position)
    print("Total Distance is %i" %locator_distance)
    curve_radius = locator_distance/2
    make_curve.tread_curve = cmds.circle(n = "TreadCurve", r = curve_radius, nr = (1, 0, 0))
    make_curve.locator_group = cmds.group(make_locator.front_locator, make_locator.back_locator, n = "Loc_Group")
    cmds.select(make_curve.tread_curve, r = True)
    cmds.select("Loc_Group", add = True)
    cmds.align(z = "mid", atl = True)
    cmds.select(make_curve.tread_curve)
    cmds.FreezeTransformations()
    cmds.textFieldButtonGrp(window_maker.text_button, edit = True, enable = True, visible = True)
    cmds.button(window_maker.curve_button, edit = True, enable = False, visible = False)
    cmds.select(clear=True)
    cmds.confirmDialog(title="Tread",message="Select an object to be the tread")
    #delete the values of selected_object

    
    cmds.select("TreadFull")
    wireObj = cmds.ls(sl = True, o = True)[0]
    
    cmds.select(make_curve.tread_curve)
    wireCurve = cmds.ls(sl = True, o = True)[0]
    
    create_wireDeformer(wireObj, wireCurve, 40)
    return updateCopynum
    

    
    ### Auto Wheel Functions ###
def master_group():
    if cmds.objExists('main_grp')!=True: # If doens't not exist create a group called "main_grp"
        cmds.group(n='main_grp', empty=True)
        cmds.select('main_grp', replace=True)
        lock_xform_channel()
    else:
        pass # if the global control already exist "pass"
        
def master_CTRL():
        if cmds.objExists('world_ctrl')!=True: # If doens't not exist create a global control
            ctrl_node = cmds.circle(degree=1, sections=6, normal=[0,1,0])
            ctrl = cmds.rename(ctrl_node[0], 'world_ctrl') # Rename transform node
            ctrl_attrs = cmds.rename(ctrl_node[1], (ctrl + '_attrs')) # Rename input node
            cmds.select(ctrl, r=True ) # Force selection of "ctrl" to resize
            resize_circle()
            #order_joints()
            global_prt = cmds.listRelatives(ctrl, p=True)
            if global_prt:
                pass
            else:
                cmds.parent(ctrl, 'main_grp')
        else:
            pass # if the global control already exist "pass"
        
def MakeJoint():
    jntList = []
    nameNumber = 1
    locList = []
    sel = cmds.ls(sl=1)
    locPosX = 0
    locPosY = 0
    locPosZ = 0
    global NewJointName
    WorldRotation = 1
    HirarchyCheckBox =0

    if NewJointName == "":
        NewJointName = "joint"
    for i in sel:
        locator = cmds.spaceLocator(n ="locator_For_Rig_"+ str(nameNumber).zfill(3))
        locList.append(locator[0])
        nameNumber += 1
        cmds.delete(cmds.parentConstraint( i , locator , mo = 0 ))
        cmds.select( clear=True )
    nameNumber = 0
    for Loc in locList:
        locPosX = cmds.getAttr(Loc+".translateX")
        locPosY = cmds.getAttr(Loc+".translateY")
        locPosZ = cmds.getAttr(Loc+".translateZ")
        newJoint = cmds.joint(p=(locPosX, locPosY, locPosZ),n = NewJointName + "_jnt_" +str(nameNumber).zfill(3))
        nameNumber += 1
        jntList.append(newJoint)
    if WorldRotation == 0:
        cmds.joint(jntList[0] ,e= True,oj = "xyz" , sao = "yup" , ch = True , zso = True )
    if HirarchyCheckBox == 0:
        for jnt in jntList:
            try:
                cmds.parent(jnt , world = True)
            except:
                print("")
        cmds.select( locList )
        cmds.delete()
        master_group()
        master_CTRL()
        
   
def getSelectedObjectSkinnedJoints():
    objects = cmds.ls(sl=True);
    cmds.select(cl=True)
    for obj in objects:
        print("-> searching for joints on: " + obj)
        skinClusters = cmds.listConnections(obj, type="skinCluster"); # how to get the skinCluster of an object??
        if (skinClusters is not None):
            for skin in skinClusters:
                print(skin)
                cmds.select(cmds.skinCluster(skin, query=True, inf=True), add=True)
                

        else:
            cmds.skinCluster(mi=1)
            print("-----> no skin on " + obj + "!")


  
def arrow_drop():
    cmds.curve(
        n = "WheelCTRL",
        d = 1, 
        p = [(-1,0,-2), (-1, 0 ,2), (-2, 0,2), (0,0,4), (2,0,2),
        (1,0,2), (1,0,-2), (2,0,-2), (0,0,-5), (-2,0,-2),(-1,0,-2)], 
        k = [0,1,2,3,4,5,6,7,8,9,10]
    )
    radial_selection = cmds.radioButtonGrp(radial_selection_button, q = True, sl = True)
    if radial_selection == 1:
        print("Direction is X")
        cmds.rotate(0,90,0)
    if radial_selection == 2:
        print("Direction is Y")
        cmds.rotate(90,0,0)
    cmds.closeCurve(rpo = True)    

def extra_arrow_drop():
    cmds.curve(
        n = "ExtraCTRL1",
        d = 1, 
        p = [(-1,0,-2), (-1, 0 ,2), (-2, 0,2), (0,0,4), (2,0,2),
        (1,0,2), (1,0,-2), (2,0,-2), (0,0,-5), (-2,0,-2),(-1,0,-2)], 
        k = [0,1,2,3,4,5,6,7,8,9,10]
    )
    radial_selection = cmds.radioButtonGrp(radial_selection_button, q = True, sl = True)
    if radial_selection == 1:
        print("Direction is X")
        cmds.rotate(0,90,0)
    if radial_selection == 2:
        print("Direction is Y")
        cmds.rotate(90,0,0)
    cmds.closeCurve(rpo = True)
        
def rename_asset():
    nameNumber = 1
    global updated_index
    curv_sel = cmds.rename("WheelCTRL","WheelCTRL_" + str(nameNumber).zfill(3))
    #cmds.rename("Wheels_Jnt_GRP",f"wheel_selection.wheel_group{updated_index}")
    
    
def unlock_channels():
    objs = cmds.ls(selection=True, type='transform')
    trs = ['t','r','s']
    xyz = ['x','y','z']
    for obj in objs:
        for attr_trs in trs:
            for axis in xyz:
                cmds.setAttr(obj + '.'+ attr_trs + axis, edit=True, lock=False)
                
                
def ik_maker():
    cmds.ls(sl=True,type='joint')
    if len(cmds.ls(sl=1, type="joint")) == 0:  # Make sure that user select the root joints
        cmds.warning('Please, first select the root joint!')
    else:
        print (actObject)
        actObject = root_ik
        print (root_ik)
        ik_selc = last_jnt
        print (last_jnt)
        rp_IK = cmds.ikHandle( sol='ikRPsolver', sj=(ik_selc), ee=(last_jnt))
        
        
def first_joint(*args):
    global actObject
    objects = cmds.ls( selection=True )
    actObject = objects[0]
    cmds.textFieldGrp('FirstJoint',edit=True,text=actObject)
    print (actObject)
    

def selc_first_joint(*args):
    print (actObject)
    print (ik_selc)


def ik_joint(*args):
    global ik_selc
    objects = cmds.ls( selection=True )
    ik_selc = objects[0]
    cmds.textFieldGrp('IKJoint',edit=True,text=ik_selc)
    print (ik_selc)
    

def of_ik_maker():
    print (root_ik_selc)
    print (last_ik)
    rp_IK = cmds.ikHandle( sol='ikRPsolver', sj=(root_ik_selc), ee=(last_ik))
    

def fk_ik_maker():
    global root_ik_selc, last_ik
    print (actObject)
    print (ik_selc)
    jts = actObject
    print (jts)
    if len(jts) ==0:  # if is not equal to 1 user is gonna get a warning
        cmds.warning('Please, first select the root joint')
    else: # if the conditions match do this:
        root_jnt = jts # show what is the root selected by user
        #pv_pos = jts[1]  # show what is the pole vector selected by user
        print (root_jnt)
        #print (pv_pos)
        cmds.select(root_jnt, replace=True) # make sure that the root joint is selected
        cmds.pickWalk(d='up') # seen if this root joint has a parent and if doens't have then the itens that we need to store is gonna be placed elsewhere
        prt_main = cmds.ls(selection=True, type='transform') # if we find the parent we gonna store in this VAR
        print (prt_main)
        rad = cmds.getAttr(root_jnt + '.radius') # looking for the radius of the root joint and getting the attribute value if we want to change
        if cmds.objExists('main_grp')!=True: # If doens't not exist create a group called "main_grp"
            cmds.group(n='main_grp', empty=True)
            cmds.select('main_grp', replace=True)
            lock_xform_channel()
        else:
            pass # if the global control already exist "pass"
        if cmds.objExists('world_ctrl')!=True: # If doens't not exist create a global control
            ctrl_node = cmds.circle(degree=1, sections=6, normal=[0,1,0])
            ctrl = cmds.rename(ctrl_node[0], 'world_ctrl') # Rename transform node
            ctrl_attrs = cmds.rename(ctrl_node[1], (ctrl + '_attrs')) # Rename input node
            cmds.select(ctrl, r=True ) # Force selection of "ctrl" to resize
            resize_circle()
            #order_joints()
            global_prt = cmds.listRelatives(ctrl, p=True)
            if global_prt:
                pass
            else:
                cmds.parent(ctrl, 'main_grp')
        else:
            pass # if the global control already exist "pass"
        resizers = root_jnt + '_control_resize_grp' # we are creating the others groups for the skeleton and controls
        skeleton = root_jnt + '_skeleton'
        controls = root_jnt + '_controls'
        world_ctrl = 'world_ctrl'
        if cmds.objExists(skeleton)!=True: # cheking if already exist a "_skeleton" group
            cmds.group(n=skeleton, empty=True)
            cmds.select(skeleton, replace=True)
            lock_xform_channel()
        else:
            pass
        if cmds.objExists(controls)!=True: # cheking if already exist a "_controls" group
            cmds.group(n=controls, empty=True)
            cmds.select(controls, replace=True)
            lock_xform_channel()
        else:
            pass
        if cmds.objExists(resizers)!=True: # cheking if already exist a "_resizers" group
            cmds.group(n=resizers, empty=True)
            cmds.select(resizers, replace=True)
            lock_xform_channel()
        else:
            pass
        fkIK = root_jnt.split('_skin')[0] + '_fkIK' # FK/IK Channels stores in a VAR the name of IK/FK channel (rename "_skin" and replace with ik/fk)
        print (fkIK)
        cmds.addAttr(world_ctrl, longName=fkIK, attributeType='double', min=0, max=1, dv=1) # creating a floating parameter for IK/FK
        cmds.setAttr((world_ctrl + '.' + fkIK), e=True, k=True) # Use the name of the root joint and set to channel box
        cmds.parent(skeleton, controls, world_ctrl)# Store controls and skeleton under global control (the last object is wat will be parent in this case "world_ctrl")
        rad_offset = 1 # VAR that we can resize the radius of the joints chain when we need
        rad_root = cmds.getAttr(root_jnt + '.radius')
        cmds.select(root_jnt, r=True)# FK chain (select the root and then duplicate the chain)
        cmds.duplicate(rr=True) # "rr"= duplicate this object as it's
        root_fk_node = cmds.ls(sl=True, type='joint')[0]
        print (root_fk_node)
        root_fk = cmds.rename(root_fk_node, (root_jnt.split('_skin')[0] + '_fk')) # renaming the duplicated joint
        cmds.select(hierarchy=True) # select all joints with hierarchy
        cmds.select(root_fk, tgl=True) # tgl off the selection of the root
        fk_chain = cmds.ls(sl=True, type='joint')
        print (fk_chain)
        for each_fk in fk_chain:
            cmds.setAttr(each_fk + '.radius', (rad_root + rad_offset)) # increase radius of the root FK
        cmds.select(hi=True) # select all joints with hierarchy
        str_skin = '_skin'
        str_fk = '_fk'
        rename_search_replace(fk_chain, str_skin, str_fk)
        cmds.select(root_jnt, r=True)# IK chain
        cmds.duplicate(rr=True)
        root_ik_node = cmds.ls(sl=True, type='joint')[0]
        root_ik = cmds.rename(root_ik_node, (root_jnt.split('_skin')[0] + '_ik'))
        cmds.select(root_ik, hi=True)
        ik_chain = cmds.ls(sl=True, type='joint')
        for each_ik in ik_chain:
            cmds.setAttr(each_ik + '.radius', (rad_root + rad_offset +1)) # increase radius of the root IK
        cmds.select(hi=True)
        cmds.select(root_fk, tgl=True)
        str_skin = '_skin'
        str_ik = '_ik'
        rename_search_replace(ik_chain, str_skin, str_ik)
        renamed_root_ik = cmds.select(root_ik, hi=True)
        renamed_ik_chain = cmds.ls(sl=True, type='joint')
        print ('RENAMED:', renamed_ik_chain)
        cmds.select(root_jnt, hi=True) # we gonna deselect the end joint
        chain = cmds.ls(sl=True, type='joint')
        size_chain = len(chain)
        cmds.select(chain[size_chain-1], tgl=True)
        main_chain = cmds.ls(sl=True, type='joint') # store the joints in a VAR
        print (main_chain)
        for each_main in main_chain: # Blend betwwen IK/FK
            jnt_prefix = each_main.split('_skin')[0] # VAR the ignores the "_skin" on the name
            print(jnt_prefix)
            rev = cmds.createNode('reverse', n=(jnt_prefix  + '_ik_rev')) # turn off the system that is not been used, if is 0 fk is gonna work and 1 is IK
            print(rev)
            ik = jnt_prefix + '_ik'
            fk = jnt_prefix + '_fk'
            prtc = cmds.parentConstraint(fk, ik, each_main)[0] # we get an average between IK/FK
            cn_wgt = cmds.parentConstraint(prtc, q=True, wal=True) # Store parent constraint weight values channels in VAR. "cn_weight"
            fk_wgt = cn_wgt[0]
            ik_wgt = cn_wgt[1]
            cmds.connectAttr((world_ctrl + '.' + fkIK), (prtc + '.' + ik_wgt), f=True) # connect attribute to the global controls and we have an IK/FK system 0 to 1
            cmds.connectAttr((world_ctrl + '.' + fkIK), (rev + '.inputX'), f=True)
            cmds.connectAttr((rev + '.outputX'), (prtc + '.' + fk_wgt), f=True)
            cmds.setAttr((fk + '.visibility'),0) # toggle off the visibility of IK/FK joints chain
            cmds.setAttr((ik + '.visibility'),0)
        cmds.select(root_fk, hi=True)
        fk_skel = cmds.ls(sl=True, type='joint')
        size_fk_skel = len(fk_skel)
        cmds.select(fk_skel, r=True)
        cmds.select(fk_skel[size_fk_skel-1], tgl=True)
        fk_skel_ctrl = cmds.ls(sl=True, type='joint') # store the chain of joints
        print (fk_skel_ctrl)
        fk_root_sel = cmds.ls(sl=True, type='joint')[0]
        print (fk_root_sel)
        fk_rg()
        fkIk_chn = world_ctrl + '.' + fkIK
        print(fkIk_chn)
        rev_fk = cmds.createNode('reverse', n=(root_fk + '_rev')) # turn off the visibility of the control object
        print (rev_fk)
        connet_rev = cmds.connectAttr(fkIk_chn, (rev_fk + '.inputX'), f=True)
        print (connet_rev)
        for each_fk_ctrl in fk_skel_ctrl: # store the controls/resizers objcts in the control/resize groups
            cmds.parent((each_fk_ctrl + '_CTRL_grp', controls))
            cmds.parent((each_fk_ctrl + '_CTRL_resize', resizers))
            cmds.connectAttr((rev_fk + '.outputX'),(each_fk_ctrl + '_CTRL_grp.visibility'), f=True)  # Toggle FK controls, so when you are using in IK controls you don't see FK controllers
        print (actObject)
        root_sel = cmds.select(actObject [:-4] + 'ik')
        root_ik_selc = cmds.ls(sl=True)[0]
        print(root_ik_selc)
        print (ik_selc)
        last_sel = cmds.select(ik_selc [:-4] + 'ik')
        last_ik = cmds.ls(sl=True)[0]
        print(last_ik)
        selection_r = cmds.select(root_ik_selc, last_ik, r=True) # IK controls, here wue select the ik chain and see the lenth to subtract 1 and always create the Ikhandle before the end joint
        print (selection_r)
        #ik_maker()
        of_ik_maker()
        ik_hdl = cmds.ls(sl=True, type='transform')[0]# store the selection of IK_handle
        print (ik_hdl)
        cmds.setAttr(ik_hdl + '.visibility', 0)
        cmds.select(ik_hdl, r=True) # force the selection of the ik handle
        ik_rg()  # create the ik control
        toggle_ik_fk = cmds.connectAttr(fkIk_chn, (ik_hdl + '_ik_CTRL_grp.visibility'), f=True) # Toggle IK controls, so when you are using in FK controls you don't see IK controllers
        cmds.connectAttr(fkIk_chn, (ik_hdl + '.ikBlend'), f=True)
        print (toggle_ik_fk)
        cmds.parent((ik_hdl + '_ik_CTRL_grp'), controls)
        cmds.parent((ik_hdl + '_ik_CTRL_resize'), resizers)
        cmds.parent(resizers,  'main_grp')
        if prt_main[0]==root_jnt:
            cmds.parent(root_jnt,root_ik, root_fk, skeleton)
        else:
            pass


def control_to_pol():
    sel_joint = cmds.ls(sl=True,type='joint')
    pole_ctrl = sel_joint[0].split('_Jnt')
    name_pol = pole_ctrl[0]

    pol_grp = cmds.group(em=True,n=name_pol + '_polv_offset')
    pol_vec_grp = cmds.group(em=True,n=name_pol + '_pol_constraint')
    pol_SDK = cmds.group(em=True,n=name_pol + '_polv_SDK')
    joint_pos = cmds.xform(sel_joint,q=True,t=True,ws=True)
    pole_v_oficial = cmds.circle(n=name_pol + '_pol_vec', nr=(0,1,0))
    pole_v_ctrl = cmds.circle(n=name_pol + '_pol', nr=(0,1,0))
    cmds.setAttr(pole_v_ctrl[0] + '.visibility', 0)
    cmds.scale(0,0,0,pole_v_ctrl)
    paren_pol = cmds.parent(pol_grp,'world_ctrl')
    paren_pol = cmds.parent(pole_v_ctrl[0],pol_vec_grp)
    paren_pol = cmds.parent(pole_v_oficial[0],pol_SDK)
    paren_pol = cmds.parent(pol_vec_grp,pol_grp)
    cmds.scale(3,3,3,pole_v_oficial)

    cmds.move(joint_pos[0],joint_pos[1],joint_pos[2],pol_grp)
    cmds.move(joint_pos[0],joint_pos[1]+13,joint_pos[2],pol_SDK)
    cmds.parentConstraint(sel_joint,pol_grp,mo=False)
    cmds.delete(pol_grp + '_parentConstraint1')
    cmds.select(pol_vec_grp)
    cmds.move(0,-20,0,r=True,os=True,wd=True)
    paren_pol = cmds.parent(pol_SDK,pol_grp)

    cmds.parentConstraint(pole_v_oficial,pole_v_ctrl,mo=1)

def pole_vector():
    list_of_curvs = cmds.ls(sl=True,type='transform')
    iks = cmds.select('ikHandle*')
    list_iks = cmds.ls(sl=True,type='ikHandle')

    for curvs,hndl in zip(list_of_curvs,list_iks):
        cmds.poleVectorConstraint (curvs, hndl)


def follow_ctrl():
    list_of_ctrls = cmds.ls(sl=True,type='transform')
    ctrls_n = list_of_ctrls[-8:]
    ctrls_d = list_of_ctrls[:8]


    for ctrls,grps in zip(ctrls_d,ctrls_n):
        cmds.pointConstraint(ctrls, grps,mo=1,weight=1)


### Window UI ###
def window_maker():
    pass
    
win_name = 'Auto_IK_FK'
if cmds.window(win_name, query=True, exists=True):
    cmds.deleteUI(win_name)
   
cmds.window(win_name, sizeable=False, height=300, width=260, backgroundColor=(0.1,0.1,0.1))


# Create the tabLayout
tabControls = cmds.tabLayout()

# Arm tab
tab1Layout = cmds.columnLayout()
    # Button for Locators
msg_002 = cmds.text('Locators goes to the avarage vertex selection')
cmds.separator(height=10)
cmds.rowLayout (cw3 = (50, 280, 40), nc = 4)
make_locators = cmds.button(label='Make Locators', w=80, h=20,enable=True, command='locator_pivot()', backgroundColor=(0.3,0.3,0.3))
cmds.separator(w=40,height=1)
reset_loc_btn = cmds.button(label='Undo Locators', w=80, h=20,enable=True, command='delete_locators()', backgroundColor=(0.3,0.3,0.3))
cmds.setParent( '..' )  

    # Button to name joints
cmds.separator(height=10)
msg_003 = cmds.text('Always change the name before creating',bgc = (1,1,0))
msg_004 = cmds.text('a new chain of joints! CONFIRM NAME!',bgc = (1,1,0))
cmds.rowLayout (cw3 = (50, 280, 40), nc = 4)
joint_name = cmds.textFieldGrp(w=100, h=20,text="JointsName", cc="name_user = cmds.textFieldGrp(joint_name, q=1, tx=1)")
cmds.separator(w=20,height=1)
confirm_name = cmds.button(label='Confirm Name', w=80, h=20,enable=True, command='name_user = cmds.textFieldGrp(joint_name, q=1, tx=1)', backgroundColor=(0.3,0.3,0.3))
cmds.setParent( '..' ) 

    # Button to create joints/show axis joints or Hide
cmds.separator(height=10)
msg_005 = cmds.text('Create Joints')
cmds.rowLayout (cw3 = (50, 280, 40), nc = 5)
make_joint_btn = cmds.button(l='Make joints', w=70, h=20,enable=True,c='make_joints()', backgroundColor=(0.3,0.3,0.3))
cmds.separator(w=10,height=1)
show_axis_joints = cmds.button(label='Show axis joints', w=90, h=20,enable=True, command='show_axis_display(display=True)', backgroundColor=(0.3,0.3,0.3))
cmds.separator(w=10,height=1)
hide_axis_joints = cmds.button(label='Hide axis joints', w=90, h=20,enable=True, command='hide_axis_display(display=False)', backgroundColor=(0.3,0.3,0.3))
cmds.setParent( '..' )

    # IK/FK
cmds.separator(height=10)
cmds.rowLayout (cw3 = (50, 280, 40), nc = 4)
cmds.textFieldGrp('FirstJoint',w=100, h=20, text='First Joint')
cmds.textFieldGrp('IKJoint',w=100, h=20, text='ik Handle Joint')
cmds.setParent( '..' )

cmds.rowLayout (cw3 = (50, 280, 40), nc = 4)
cmds.button('FistJointButton', label='<',w=70, h=20,command=first_joint,backgroundColor=(0.3,0.3,0.3))
cmds.separator(w=50,height=1)
cmds.button('IKJointButton', label='<',w=70, h=20,command=ik_joint,backgroundColor=(0.3,0.3,0.3))
cmds.setParent( '..' )

cmds.separator(height=10)
msg_006 = cmds.text('IK/FK Switcher')
cmds.rowLayout (cw3 = (50, 280, 40), nc = 4)
MAKE_FK_BTN = cmds.button(label='Make FK/IK', w=70, h=20,enable=True, command='fk_ik_maker()', backgroundColor=(0.3,0.3,0.3))
cmds.separator(w=50,height=1)
cmds.setParent( '..' )

cmds.separator(height=10)
msg_006 = cmds.text('Pole Vector')
cmds.rowLayout (cw3 = (50, 280, 40), nc = 7)
create_controllers = cmds.button(label='control', w=70, h=20,enable=True, command='control_to_pol()', backgroundColor=(0.3,0.3,0.3))
cmds.separator(w=10,height=1)
create_controllers = cmds.button(label='pole vector', w=70, h=20,enable=True, command='pole_vector()', backgroundColor=(0.3,0.3,0.3))
cmds.separator(w=10,height=1)
create_controllers = cmds.button(label='follow ctrl', w=70, h=20,enable=True, command='follow_ctrl()', backgroundColor=(0.3,0.3,0.3))
cmds.separator(w=10,height=1)
cmds.setParent( '..' )
cmds.rowLayout (cw3 = (50, 280, 40), nc = 2)
cmds.separator(height=50)
SEL_GLOBAL_BTN = cmds.button(label='Select world_ctrl', w=110, h=20,enable=True, command='select_world_ctrl()', backgroundColor=(0.3,0.3,0.3))
cmds.setParent( '..' )

cmds.separator(height=10)
msg_007 = cmds.text('After you create the joints')
msg_008 = cmds.text('you can press:"Undo Locators"')
cmds.separator(height=10)

cmds.iconTextButton("lblCopyright1", l="All Rights Reserved.", w=290, h=20, style="textOnly", c="cmds.showHelp(\"http://www.arthurcurymeirelle.wixsite.com/art3d\", a=1)",backgroundColor=(0.3,0.3,0.3))
# We need to go back one to the tabLayout (the parent) to add the next tab layout.
cmds.setParent('..')


# Create appropriate labels for the tabs
cmds.tabLayout(tabControls, edit=True, tabLabel=(
(tab1Layout, "IK FK Maker")))


cmds.showWindow('Auto_IK_FK')
