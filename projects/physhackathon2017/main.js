"use strict";

// GLOBALS ------------------------------------------------------------
var camera, scene, renderer, controls, axis, clock;

var width = 1024;
var height = 768;
var windowHalfX = width / 2;
var windowHalfY = height / 2;

var grid = [], sources = [], gridMaterials;
var currentTime = 0;
var dotGeometry;

var gridWidth = 200, gridHeight = 200;
var spheres = [];

var FPS = 90;

function addSource() {
	params.numSource++;
	addSrc(Math.round(Math.random()*200),Math.round(Math.random()*200),Math.random()*4.0-2,0,0);
}

var sourceA = {
	x : 175,
	y : 25,
	phase : 0,
	vx : 0,
	vy : 0,
	fx : 0.0,
	fy : 0.0
}

var sourceB = {
	x : 25,
	y : 175,
	phase : 0,
	vx : 0,
	vy : 0,
	fx : 0.0,
	fy : 0.0
} 

//colors---------------------------------
var Config=function(input){
    this.color = input;
}

var colorsTop = new Config("#ffffff");
var colorsBot = new Config("#000000");

var rgbTop = {
	r: 255,
	g: 0,
	b: 0
}

var rgbBot = {
	r: 0,
	g: 0,
	b: 255
}

function ConvertRgb(r,g,b,rgb) {
	rgb.r = r;
	rgb.g = g;
	rgb.b = b;
}

//update color 
function updateColor(hex,rgb) {
	var colorValue = parseInt ( hex.replace("#","0x"), 16 );
	var Cool = new THREE.Color(colorValue);
	ConvertRgb(Cool.r,Cool.g,Cool.b,rgb);
}

function calculateColor(x,y) {
	var ratio = (10+grid[x][y]*1.0)/20;
    var Red =  (rgbBot.r + ((rgbTop.r - rgbBot.r)*ratio));
    var Green = (rgbBot.g + ((rgbTop.g - rgbBot.g)*ratio));
    var Blue = (rgbBot.b + ((rgbTop.b - rgbBot.b)*ratio));
    return [Red,Green,Blue];
}

// EVENTS ------------------------------------------------------------
document.addEventListener("load", onLoad());
function onLoad() {
	init();
}

document.addEventListener("keypress", function(e) {
	if(e.key == 'a') {
		axis[0].visible = !axis[0].visible;
		axis[1].visible = !axis[1].visible;
		axis[2].visible = !axis[2].visible;
	}
});

window.addEventListener( 'resize', onWindowResize, false );
function onWindowResize( event ) {
	renderer.setSize( width, height );

	camera.aspect = width / height;
	camera.updateProjectionMatrix();
}

function onRender()
{
	setTimeout( function() {
        requestAnimationFrame( onRender );
    }, 1000 / FPS );
    if(!params.Freeze){
    	onUpdate();
    }
	renderer.render(scene, camera);
}

// --------------------------------------------------------------------
function init()
{
	// camera
	var container = document.getElementById( 'container' );

	camera = new THREE.PerspectiveCamera( 40, windowHalfX / windowHalfY, 1, 3000 );
	camera.up.set(0,0,1);
	camera.position.x = 356;
	camera.position.y = 395;
	camera.position.z = 100;
	camera.lookAt(new THREE.Vector3(0,-100,-100));

	scene = new THREE.Scene();
	renderer = new THREE.WebGLRenderer( { antialias: true } );
	renderer.setPixelRatio( window.devicePixelRatio );
	container.appendChild( renderer.domElement );
	renderer.autoClear = false;

	// controls
	controls = new THREE.OrbitControls(camera, renderer.domElement);

	// 3D-axis
	var K = 10;
	var matX = new THREE.LineBasicMaterial({color:0xff0000});
	var matY = new THREE.LineBasicMaterial({color:0x00ff00});
	var matZ = new THREE.LineBasicMaterial({color:0x0000ff});
	var geometryX = new THREE.Geometry();
	geometryX.vertices.push(new THREE.Vector3(0, 0, 0));
	geometryX.vertices.push(new THREE.Vector3(K, 0, 0));
	var lineX = new THREE.Line(geometryX, matX);
	scene.add(lineX);
	var geometryY = new THREE.Geometry();
	geometryY.vertices.push(new THREE.Vector3(0, 0, 0));
	geometryY.vertices.push(new THREE.Vector3(0, K, 0));
	var lineY = new THREE.Line(geometryY, matY);
	scene.add(lineY);
	var geometryZ = new THREE.Geometry();
	geometryZ.vertices.push(new THREE.Vector3(0, 0, 0));
	geometryZ.vertices.push(new THREE.Vector3(0, 0, K));
	var lineZ = new THREE.Line(geometryZ, matZ);
	scene.add(lineZ);
	axis = [lineX, lineY, lineZ];

	clock = new THREE.Clock();

	gui_init();
	createScene();
	onRender();

	onWindowResize();
}

function createScene()
{
	// create grid
	createGrid(gridWidth, gridHeight);

	addSrc(sourceA.x, sourceA.y, 0, sourceA.vx, sourceA.vy);
	addSrc(sourceB.x, sourceB.y, 0, sourceB.vx, sourceB.vy);
	
	dotGeometry = new THREE.BufferGeometry();

	var vertices = new Float32Array(3*gridWidth*gridHeight);
	var colors = new Float32Array(3*gridWidth*gridHeight);
	for (var x = 0; x < gridWidth; ++x)
	{
		for (var y = 0; y < gridHeight; ++y)
		{
			var index = (x*gridWidth) + y;
			vertices[index] = x;
			vertices[index+1] = y;
			vertices[index+2] = 0;
			colors[index] = 1;
			colors[index+1] = 1;
			colors[index+2] = 1;
		}
	}

	dotGeometry.addAttribute('position', new THREE.BufferAttribute( vertices, 3 ));
	dotGeometry.addAttribute('color', new THREE.BufferAttribute( colors, 3 ));
	var pointsMaterial = new THREE.PointsMaterial( { size: 2, sizeAttenuation: false, vertexColors: THREE.VertexColors } );
	var dot = new THREE.Points( dotGeometry, pointsMaterial );

	scene.add(dot);
}
document.addEventListener( 'mousedown', onDocumentMouseDown );

function onDocumentMouseDown( event ) {
	var rect = document.getElementById( "container" ).getBoundingClientRect();
    var mouse2D = new THREE.Vector2(
    	( event.clientX-rect.left / rect.width ) * 2 - 1,
        -( event.clientY-rect.top / rect.height ) * 2 + 1
        );

    var raycaster = new THREE.Raycaster()
	raycaster.setFromCamera(mouse2D,camera);

    var intersects = raycaster.intersectObjects( spheres );

    if ( intersects.length > 0 ) {
        intersects[ 0 ].object.material.color.setHex( 0xffff00 );
    }
}

function onUpdate()
{
	//update the sources
	for (var i = 0; i < sources.length; ++i)
	{
		updateSource(i,sources[i].x,sources[i].y,sources[i].phase,sources[i].vx,sources[i].vy,sources[i].fx,sources[i].fy);
	}
	updateColor(colorsTop.color,rgbTop);
	updateColor(colorsBot.color,rgbBot);

	renderer.setClearColor(new THREE.Color(0,0,0));
	renderer.clear();

	controls.update();

	tickSim(currentTime, sources, params.frequency_hz, params.WaveSpeed_MperSec, params.amplitude_m,params.DampingSpeed_MperSec,params.dt);

	for (var x = 0; x < grid.length; ++x)
    {
        for (var y = 0; y < grid[x].length; ++y)
        {
        	var ratio = (10+grid[x][y]*1.0)/20;
            var index = 3*((x*gridHeight)+y);
            if (!params.soundCompressionMode)
            {
            	dotGeometry.attributes.position.set([x,y,grid[x][y]], index);
            	dotGeometry.attributes.color.set(calculateColor(x,y), index);
        	}
        	else
        	{
            	dotGeometry.attributes.position.set([x+ratio * 5.0,y-ratio * 5.0,0], index);
            	dotGeometry.attributes.color.set([1,1,1], index);
            	params.numSource = 1;
        	}
        }
    }
    dotGeometry.attributes.position.needsUpdate = true;
    dotGeometry.attributes.color.needsUpdate = true;
}

function addSrc(x,y,phase,vx,vy)
{
	sources.push({
		'x' : x,
		'y' : y,
		'phase' : phase,
		'vx' : vx,
		'vy' : vy,
		'fx' : x,
		'fy' : y
	});
	var geometry = new THREE.SphereGeometry(5,32,32);
    var material = new THREE.MeshBasicMaterial( { color: 0xff0000 } );
	var sphere = new THREE.Mesh( geometry, material );
    spheres.push(sphere);
    scene.add( sphere );
    sphere.position.set(sources[sources.length-1].x, sources[sources.length-1].y, 0);
    sphere.visible = true;

    gui_addSource(sources);
}

//as advertised, we update the sources
function updateSource(index,NewX,NewY,phase,vx,vy,fx,fy)
{
	sources[index].x = NewX;
	sources[index].y = NewY;
	sources[index].phase = phase;
	sources[index].vx = vx;
	sources[index].vy = vy;
	sources[index].fx = fx;
	sources[index].fy = fy;
	spheres[index].position.set(fx, fy, grid[NewX][NewY]);
}
