bl_info = {
    "name": "Euler to Quaternion Helper",
    "blender": (3, 6, 21),  # Blender version this is compatible with
    "category": "Animation",
    "author": "Liam Shelton",
    "version": (1, 0, 0),
    "description": "Adds a Pose button that changes the rotation mode of the selected bone to Quaternions, inserts a keyframe, and restores the original mode, to speed up the process of turning Euler keyframes into Quaternions.",
}

import bpy

# Define the operator to execute the logic
class OBJECT_OT_insert_rotation_keyframe(bpy.types.Operator):
    bl_idname = "object.insert_rotation_keyframe"
    bl_label = "Convert Euler Keyframe to Quaternion"

    def execute(self, context):
        armature = bpy.context.object

        # Check if the selected object is an armature
        if armature and armature.type == 'ARMATURE':
            # Get the active bone
            active_bone = armature.pose.bones.get(armature.data.bones.active.name)

            if active_bone:
                # Store the current rotation mode to restore later
                previous_rotation_mode = active_bone.rotation_mode
                
                # Set the rotation mode of the active bone to 'QUATERNION'
                active_bone.rotation_mode = 'QUATERNION'
                print(f"Rotation mode of the bone '{active_bone.name}' set to 'QUATERNION'.")

                # Insert a rotation keyframe for the selected bone at the current frame
                active_bone.keyframe_insert(data_path="rotation_quaternion", frame=bpy.context.scene.frame_current)
                print(f"Rotation keyframe inserted at frame {bpy.context.scene.frame_current}.")

                # Restore the original rotation mode of the active bone
                active_bone.rotation_mode = previous_rotation_mode
                print(f"Rotation mode of the bone '{active_bone.name}' restored to '{previous_rotation_mode}'.")
                
                return {'FINISHED'}
            else:
                self.report({'WARNING'}, "No active bone found.")
                return {'CANCELLED'}
        else:
            self.report({'WARNING'}, "No armature is selected.")
            return {'CANCELLED'}

# Define the panel that will hold the button in the Pose menu
class VIEW3D_PT_pose_keyframe_panel(bpy.types.Panel):
    bl_label = "Bone Rotation Keyframe"
    bl_idname = "VIEW3D_PT_pose_keyframe_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Pose'
    bl_context = "posemode"  # Ensure it only appears in Pose Mode

    def draw(self, context):
        layout = self.layout

        # Add a button to the panel that will call the operator
        layout.operator("object.insert_rotation_keyframe")
def menu_func(self, context):
    self.layout.operator(OBJECT_OT_insert_rotation_keyframe.bl_idname)


def register():
    bpy.utils.register_class(OBJECT_OT_insert_rotation_keyframe)
    bpy.types.VIEW3D_MT_pose.append(menu_func)


def unregister():
    bpy.utils.unregister_class(OBJECT_OT_insert_rotation_keyframe)
    bpy.types.VIEW3D_MT_pose.remove(menu_func)

# Run the register function when the addon is enabled
if __name__ == "__main__":
    register()
