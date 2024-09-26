# -------------------- IMPORTS --------------------

import bpy

# -------------------- INFORMATION --------------------

bl_info = {
    "name": "Mass DataBlock Split",
    "author": "Moonlight_",
    "version": (1, 0, 0),
    "blender": (2, 80, 0),
    "category": "Object",
    "location": "3D Viewport > Sidebar > data-block converter",
    "description": "Separate objets who share the same data-block into unique data-blocks for each of these objects",
    "doc_url": "github.com/leonardostefanello/Blender-Polygon-Selector/blob/main/README.md",
    "tracker_url": "github.com/leonardostefanello/Blender-Polygon-Selector/issues",
}

# -------------------- SETUP --------------------

# Class to store data of objects with shared data-blocks
class SharedObjectItem(bpy.types.PropertyGroup):
    object_ref: bpy.props.PointerProperty(type=bpy.types.Object)

class OBJECT_OT_Verify(bpy.types.Operator):
    bl_idname = "object.verify"
    bl_label = "Verify Objects"
    
    def execute(self, context):
        props = context.scene.my_addon_props
        props.obj_verified = 0
        props.obj_with_data_block = 0

        # Clear the collection of shared data-block objects
        props.shared_objects.clear()

        # Dictionary to store how many times each data-block is referenced
        data_blocks = {}

        # Check all objects in the current scene
        for obj in bpy.data.objects:
            if obj.type == 'MESH':
                props.obj_verified += 1
                mesh_data = obj.data
                if mesh_data in data_blocks:
                    data_blocks[mesh_data].append(obj)
                else:
                    data_blocks[mesh_data] = [obj]

        # Count objects sharing the same data-block
        for objs in data_blocks.values():
            if len(objs) > 1:
                props.obj_with_data_block += len(objs)
                for obj in objs:
                    item = props.shared_objects.add()
                    item.object_ref = obj
        
        return {'FINISHED'}

class OBJECT_OT_Fix(bpy.types.Operator):
    bl_idname = "object.fix"
    bl_label = "Fix Objects"

    def execute(self, context):
        props = context.scene.my_addon_props
        props.obj_fixed = 0

        for item in props.shared_objects:
            obj = item.object_ref
            if obj and obj.data.users > 1:
                obj.data = obj.data.copy()
                props.obj_fixed += 1

        return {'FINISHED'}

class OBJECT_OT_Clear(bpy.types.Operator):
    bl_idname = "object.clear"
    bl_label = "Clear Info"
    
    def execute(self, context):
        props = context.scene.my_addon_props
        props.obj_verified = 0
        props.obj_with_data_block = 0
        props.obj_fixed = 0
        props.shared_objects.clear()
        return {'FINISHED'}

class Properties(bpy.types.PropertyGroup):
    obj_verified: bpy.props.IntProperty(name="Objects Verified")
    obj_with_data_block: bpy.props.IntProperty(name="Objects with Shared Data Block")
    obj_fixed: bpy.props.IntProperty(name="Objects Fixed")
    shared_objects: bpy.props.CollectionProperty(type=SharedObjectItem)

class OBJECT_PT_CustomPanel(bpy.types.Panel):
    bl_label = "Mass DataBlock Split"
    bl_idname = "OBJECT_PT_custom_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Mass DataBlock Split'

    def draw(self, context):
        layout = self.layout
        props = context.scene.my_addon_props

        layout.label(text=f"Objects Verified: {props.obj_verified}")
        layout.label(text=f"Objects with Shared Data Block: {props.obj_with_data_block}")
        layout.label(text=f"Objects Fixed: {props.obj_fixed}")

        row = layout.row()
        row.operator("object.verify", text="Verify")

        row = layout.row()
        row.operator("object.fix", text="Fix")

        row = layout.row()
        row.operator("object.clear", text="Clear")


def register():
    bpy.utils.register_class(SharedObjectItem)
    bpy.utils.register_class(OBJECT_OT_Verify)
    bpy.utils.register_class(OBJECT_OT_Fix)
    bpy.utils.register_class(OBJECT_OT_Clear)
    bpy.utils.register_class(Properties)
    bpy.utils.register_class(OBJECT_PT_CustomPanel)
    bpy.types.Scene.my_addon_props = bpy.props.PointerProperty(type=Properties)


def unregister():
    bpy.utils.unregister_class(SharedObjectItem)
    bpy.utils.unregister_class(OBJECT_OT_Verify)
    bpy.utils.unregister_class(OBJECT_OT_Fix)
    bpy.utils.unregister_class(OBJECT_OT_Clear)
    bpy.utils.unregister_class(Properties)
    bpy.utils.unregister_class(OBJECT_PT_CustomPanel)
    del bpy.types.Scene.my_addon_props

if __name__ == "__main__":
    register()

# -------------------- END --------------------