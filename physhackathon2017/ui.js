"use strict";

// GUI global variable -----------------------------------------------
var ssaoPass = {};
var params = { 
	amplitude_m: 20, 
	frequency_hz: 1, 
	WaveSpeed_MperSec: 75, 
	DampingSpeed_MperSec: 2.5,
	dt: 0.012,
	GridSizeX: 200, 
	GridSizeY: 200,
	Freeze:false,
	Source:1,
	numSource:2,
	switch_Algorithm:true,
	soundCompressionMode:false,

	AddSource : function(){ addSource();},
	Reset_Sources: function (value) {
        for (var i = 0; i < sources.length; i++) {
        gui.removeFolder('Source'+i);
    }
        resetGrid();
        resetSource();

    },
    View_Code : function(){window.location.href = 'https://github.com/kevenv/physhackathon2017';}

};
var gui;

dat.GUI.prototype.removeFolder = function(name) {
    var folder = this.__folders[name];
    if (!folder) {
        return;
    }
    folder.close();
    this.__ul.removeChild(folder.domElement.parentNode);
    delete this.__folders[name];
    this.onResize();
}
function gui_init()
{
	// Init gui
	gui = new dat.GUI({ width: 500 });
	var CodeControls = gui.addFolder('View Source Code');
	var WaveControls = gui.addFolder( 'WaveControls' );
	var ColorControls = gui.addFolder( 'Color');
	WaveControls.add(params, 'Freeze',false).onChange( function( value ) { ssaoPass.Freeze = value; } );
	WaveControls.add(params, 'amplitude_m' ).min( 0 ).max( 100 ).onChange( function( value ) { ssaoPass.amplitude_m = value; } );
	WaveControls.add(params, 'frequency_hz' ).min( 0 ).max( 2 ).onChange( function( value ) { ssaoPass.frequency_hz = value; } );
	// unit for WaveSpeed is m/s
	WaveControls.add(params, 'WaveSpeed_MperSec' ).min( 0 ).max(1000).onChange( function( value ) { ssaoPass.WaveSpeed_MperSec = value; } );
	WaveControls.add(params, 'switch_Algorithm',true).onChange( function( value ) {ssaoPass.switch_Algorithm = value; });
	WaveControls.add(params, 'DampingSpeed_MperSec',0,10,0.1).onChange( function( value ) { ssaoPass.DampingSpeed_MperSec = value; } );
	WaveControls.add(params, 'dt', 0.001,0.012,0.001).onChange( function( value ) { ssaoPass.dt = value; } );
	WaveControls.add(params, 'soundCompressionMode',false).onChange( function( value ) {ssaoPass.soundCompressionMode = value; });
	WaveControls.add(params, 'AddSource');
	WaveControls.add(params, 'Reset_Sources')

	//handling color input 
	var Top = ColorControls.addColor(colorsTop, 'color');
	var Bot = ColorControls.addColor(colorsBot, 'color');
	
	Top.onChange( function(value)
	{ 
			value=value.replace( '#','0x' );
			colorsTop.color =  value;
	});
	Bot.onChange( function(value)
	{ 
			value=value.replace( '#','0x' );
			colorsBot.color =  value;
	});
	CodeControls.add(params,'View_Code');
	WaveControls.open();
}

function gui_addSource(sources)
{
	var i = sources.length - 1;
	var sourceControl = gui.addFolder( 'Source' + i );
	sourceControl.add(sources[i], 'x', 0,200,1).onChange( function(value){ ssaoPass.x = value; });
	sourceControl.add(sources[i], 'y', 0,200,1).onChange( function(value){ ssaoPass.y = value; });
	sourceControl.add(sources[i], 'phase').min(-2).max(2).onChange( function(value){ ssaoPass.phase = value; });
	sourceControl.add(sources[i], 'vx').min(-40).max(40).onChange( function(value){ ssaoPass.vx = value; });
	sourceControl.add(sources[i], 'vy').min(-40).max(40).onChange( function(value){ ssaoPass.vy = value; });
}
