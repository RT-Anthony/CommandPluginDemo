import project_path
import maya.api.OpenMaya as OpenMaya
from maya import cmds
import maya.mel as mel
import sys
import os
from assets_pipe import assets_pipe
from project_path import project_path
from inject_asset import inject_asset_maya


class RTAvailableAssetList(OpenMaya.MPxCommand):
    kPluginCmdName = "rtAvailableAssetList"
    
    def __init__(self):
        OpenMaya.MPxCommand.__init__(self)
		
    @staticmethod
    def cmdCreator():
        return RTAvailableAssetList()
		
    def doIt(self, args):
        asset_list = []
        pipe = assets_pipe.read_assets_pipe()
        for asset in pipe.assets:
            asset_list.append(asset.name)
        self.setResult(asset_list) 


class RTInjectAsset(OpenMaya.MPxCommand):
    kPluginCmdName = "rtInjectAsset"
    
    def __init__(self):
        OpenMaya.MPxCommand.__init__(self)
		
    @staticmethod
    def cmdCreator():
        return RTInjectAsset()

    @staticmethod
    def syntaxCreator():
        syntax = OpenMaya.MSyntax()
        syntax.addFlag("-n", "-name", OpenMaya.MSyntax.kString)
        return syntax

    def parseArgs(self, args):
        argData = OpenMaya.MArgParser(self.syntax(), args)
        if argData.isFlagSet( "-n" ):
            name = argData.flagArgumentString("-n", 0)
        return name
		
    def doIt(self, args):
        backend = inject_asset_maya.InjectAssetBackend()
        name = self.parseArgs(args)
        backend.inject_asset_info.asset_name = name
        backend.inject_asset_info.asset_path = project_path.get_asset_folder(name)
        backend.inject_asset_info.representation_name = "Final"
        backend.inject_asset_info.variant_name = "Default"
        offset_info = backend.generate_offset_info(0, 0, 0)
        backend.inject_offset_and_update_shot_pipe(1, offset_info)


def initializePlugin( mobject ):
    ''' Initialize the plug-in when Maya loads it. '''
    mplugin = OpenMaya.MFnPlugin( mobject )
    try:
        mplugin.registerCommand( RTAvailableAssetList.kPluginCmdName, 
            RTAvailableAssetList.cmdCreator )
    	mplugin.registerCommand( RTInjectAsset.kPluginCmdName, 
            RTInjectAsset.cmdCreator, RTInjectAsset.syntaxCreator )
    except:
        sys.stderr.write( 'Failed to register command(s)')


def uninitializePlugin( mobject ):
    ''' Uninitialize the plug-in when Maya un-loads it. '''
    mplugin = OpenMaya.MFnPlugin( mobject )
    try:
        mplugin.deregisterCommand( RTAvailableAssetList.kPluginCmdName )
        mplugin.deregisterCommand( RTInjectAsset.kPluginCmdName )
    except:
        sys.stderr.write( 'Failed to unregister command(s)')


def maya_useNewAPI():
    """Needs to be here to tell maya to use new python api"""
    pass
