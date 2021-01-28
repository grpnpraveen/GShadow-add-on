bl_info = {
    "name": "GShadow",
    "author": "Gali_Ravi_Praveen",
    "version": (1, 0),
    "blender": (2, 91, 2),
    "location": "View3D > Toolshelf",
    "description": "Adds shadow to Gpencil",
    "warning": "",
    "doc_url": "",
    "category": "Add GShadow",
}
import bpy
#           custom properties
class GProperties(bpy.types.PropertyGroup):
    render_eng: bpy.props.EnumProperty(name="Rend_Eng",description="important",items=[('OP1',"Eevee",""),('OP2',"Cycles","")])
    shd_qlty: bpy.props.EnumProperty(name="shadow quality",description="quality",items=[('H',"Hard",""),('S',"Soft","")])
    
#           PANEL  DESIGN                                                                                  
class GShadowMainPanel(bpy.types.Panel):
    bl_label = "GShadow"
    bl_idname = "GSHADOW_PT_MAINPANEL"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'GShadow'

    def draw(self, context):
        layout = self.layout
        scene=context.scene
        mypropty=scene.ren_en
        row=layout.row()
        row.label(text="Add to only strokes.",icon="OUTLINER_OB_GREASEPENCIL")
        row=layout.row()
        row.prop(mypropty,"render_eng")
        row=layout.row() 
        row.prop(mypropty,"shd_qlty")
        row=layout.row()  
        row.operator('gshadow.shadow_operator',text="Add Shadow")

#         final reg and unregis
class GShadow_add(bpy.types.Operator):                              
    bl_label="open"
    bl_idname='gshadow.shadow_operator'

    @classmethod
    def poll(cls, context):
        return context.object is not None

    def execute(self, context):
        scene=context.scene
        mypropty=scene.ren_en
        bpy.ops.gpencil.convert(type='PATH', timing_mode='LINEAR', use_timing_data=False)
        stroke_obj=bpy.context.active_object
        x=stroke_obj.scale[0]
        str1=stroke_obj.name+"_"+"shadow"
        bpy.data.objects["Lines"].name=str1
        shadow_obj=bpy.data.objects[str1]
        shadow_obj.data.bevel_depth = 0.003*x
        if mypropty.shd_qlty=='S':
            shadow_obj.modifiers.new("subsurface",'SUBSURF')
            shadow_obj.modifiers["subsurface"].levels=2
        parnt=stroke_obj
        chld=shadow_obj
        constrnt=chld.constraints.new(type='CHILD_OF')
        constrnt.target=parnt
        if mypropty.render_eng=='OP2':
            bpy.context.scene.render.engine = 'CYCLES'
            shadow_obj.cycles_visibility.camera = False
            shadow_obj.hide_viewport = True
        else:
            new_mat=bpy.data.materials.new(name="shadow_mat")
            shadow_obj.data.materials.append(new_mat)
            new_mat.use_nodes=True
            new_mat.blend_method = 'CLIP'
            nodes=new_mat.node_tree.nodes
            principle_bsdf=nodes.get("Principled BSDF")
            principle_bsdf.inputs[19].default_value = 0
            shadow_obj.hide_viewport = True
        return {'FINISHED'}
                
def register():
    bpy.utils.register_class(GShadow_add)
    bpy.utils.register_class(GShadowMainPanel)
    bpy.utils.register_class(GProperties)
    bpy.types.Scene.ren_en=bpy.props.PointerProperty(type=GProperties)
     
def unregister():
     bpy.utils.unregister_class(GShadowMainPanel)
     bpy.utils.unregister_class(GShadow_add)
     del bpy.types.Scene.ren_en
      
if __name__ == "__main__":
    register()


    
