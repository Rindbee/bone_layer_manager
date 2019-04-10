import bpy

from .blmfuncs import store_props


class BLM_PT_customproperties(bpy.types.Panel):
    """Creates a Rig Properties Panel (Pose Bone Custom Properties) """
    bl_category = "Bone Layers"
    bl_label = "Rig Properties"
    bl_idname = "BLM_PT_customproperties"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    # bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(self, context):
        return context.mode == 'POSE'

    def draw(self, context):
        layout = self.layout


class BLM_PT_customproperties_options(bpy.types.Panel):
    """Creates a Custom Properties Options Subpanel"""
    bl_idname = "BLM_PT_customproperties_options"
    bl_label = "Display Options"
    bl_parent_id = "BLM_PT_customproperties"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'

    store_props()

    @classmethod
    def poll(self, context):
        return context.mode == 'POSE'

    def draw(self, context):
        layout = self.layout
        scn = context.scene

        row = layout.row()
        row.prop(scn, "BLM_ShowPropEdit", text="Edit Mode")
        row.prop(scn, "BLM_ShowBoneLabels", text="Bone Name")
        row.prop(scn, "BLM_ShowArmatureName", text="Armature Name")


class BLM_PT_customproperties_layout(bpy.types.Panel):
    """Displays a Rig Custom Properties in Subpanel"""
    bl_category = "Bone Layers"
    bl_label = ""
    bl_idname = "BLM_PT_customproperties_layout"
    bl_parent_id = "BLM_PT_customproperties"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_options = {"HIDE_HEADER"}

    @classmethod
    def poll(self, context):
        return context.mode == 'POSE'

    def draw(self, context):
        layout = self.layout
        pose_bones = context.active_object.pose.bones
        arm = context.active_object

        def assign_props(row, val, key, index):
            row.data_path = f"selected_pose_bones[{index}]"
            row.property = key

            try:
                row.value = str(val)
            except:
                pass

        showedit = bpy.context.scene.BLM_ShowPropEdit
        showbone = bpy.context.scene.BLM_ShowBoneLabels
        showarm = bpy.context.scene.BLM_ShowArmatureName
        has_ui = False

        active_pose_bone = context.active_pose_bone

        # Iterate through selected bones add each prop property of each bone to the panel.

        for (index, bone) in enumerate(context.selected_pose_bones):
            if (bone.keys() or showedit):
                has_ui = True
                if (showarm or showbone):
                    row = layout.row(align=True)
                    row.alignment = 'LEFT'
                    if showarm:
                        row.label(text=arm.name, icon='ARMATURE_DATA')
                        if showbone:
                            row.label(icon='RIGHTARROW')
                    if showbone:
                        row.label(icon='BONE_DATA')
                        if showedit:
                            row.emboss = 'PULLDOWN_MENU'
                            row.prop(bone, 'name', text="")
                        else:
                            row.label(text=bone.name)

            if len(bone.keys()) > 0:
                box = layout.box()
            # row = box.row()
            for key in bone.keys():
                if key not in '_RNA_UI':
                    # box = layout.box()
                    val = bone.get(key, "value")

                    row = box.row()
                    split = row.split(align=True, factor=0.3)
                    row = split.row(align=True)
                    row.label(text=key, translate=False)

                    row = split.row(align=True)
                    row.prop(bone, f'["{key}"]', text="", slider=True)

                    if showedit is True:
                        split = row.split(align=True, factor=0)

                        row = split.row(align=True)
                        row = row.operator("wm.properties_edit", text="", icon='SETTINGS')
                        assign_props(row, val, key, index)

                        row = split.row(align=False)
                        row = row.operator("wm.properties_remove", text="", icon='X')
                        assign_props(row, val, key, index)

            if showedit:
                row = layout.row(align=True)
                row.context_pointer_set('active_pose_bone', bone)
                add = row.operator("wm.properties_add", text="Add")
                add.data_path = "active_pose_bone"

        if not context.selected_pose_bones:
            layout.label(text="No bones selected", icon='INFO')
        elif not has_ui:
            layout.label(text="No available bone properties", icon='INFO')
