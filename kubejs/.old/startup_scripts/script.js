// priority: 0

console.info('Hello, World! (You will only see this line once in console, during startup)')

onEvent('item.registry', event => {
	// Register new items here
	// event.create('example_item').displayName('Example Item')
})

onEvent('block.registry', event => {
  event.create('test_block')
  	   .material('dirt')
       .hardness(0.5)
       .tagBlock('minecraft:mineable/shovel') // Make it mine faster using a shovel in 1.18.2+
  	   .tagBlock('minecraft:requries_iron_tool') // Make it require an iron or higher level tool on 1.18.2+
  	   .requiresTool(true) // Make it require a tool to drop any loot
  
  // Block with custom type (see below for list of types)
  event.create('test_block_slab', 'slab').material('glass').hardness(0.5)

  event.create('cut_scoria_brick1')
  	   .material('stone')
       .hardness(0.5)

  event.create('cut_scoria_brick2')
  	   .material('stone')
       .hardness(0.5)

  event.create('cut_scoria_brick3')
  	   .material('stone')
       .hardness(0.5)
  
  event.create('cut_scoria_brick4')
  	   .material('stone')
       .hardness(0.5)

  event.create('cut_scoria_brick5')
  	   .material('stone')
       .hardness(0.5)

  event.create('cut_scoria_brick6')
  	   .material('stone')
       .hardness(0.5)

  event.create('cut_scoria_brick7')
  	   .material('stone')
       .hardness(0.5)

  event.create('cut_scoria_brick8')
  	   .material('stone')
       .hardness(0.5)

  event.create('cut_scoria_brick9')
  	   .material('stone')
       .hardness(0.5)

  event.create('cut_scoria_brick10')
  	   .material('stone')
       .hardness(0.5)

  event.create('cut_scoria_brick11')
  	   .material('stone')
       .hardness(0.5)

  event.create('cut_scoria_brick12')
  	   .material('stone')
       .hardness(0.5)

  event.create('cut_scoria_brick13')
  	   .material('stone')
       .hardness(0.5)

  event.create('cut_scoria_brick14')
  	   .material('stone')
       .hardness(0.5)

  event.create('cut_scoria_brick15')
  	   .material('stone')
       .hardness(0.5)

  event.create('cut_scoria_brick16')
  	   .material('stone')
       .hardness(0.5)

  event.create('cut_scoria_brick17')
  	   .material('stone')
       .hardness(0.5)

  event.create('cut_scoria_brick18')
  	   .material('stone')
       .hardness(0.5)

  event.create('cut_scoria_brick19')
  	   .material('stone')
       .hardness(0.5)

  event.create('cut_scoria_brick20')
  	   .material('stone')
       .hardness(0.5)

  event.create('cut_scoria_brick21')
  	   .material('stone')
       .hardness(0.5)

  event.create('cut_scoria_brick22')
  	   .material('stone')
       .hardness(0.5)

  event.create('cut_scoria_brick23')
  	   .material('stone')
       .hardness(0.5)

  event.create('cut_scoria_brick24')
  	   .material('stone')
       .hardness(0.5)

  event.create('cut_scoria_brick25')
  	   .material('stone')
       .hardness(0.5)

  event.create('cut_scoria_brick26')
  	   .material('stone')
       .hardness(0.5)

  event.create('cut_scoria_brick27')
  	   .material('stone')
       .hardness(0.5)
  
  event.create('ablue')
       .material('stone')
       .hardness(0.5)
      
  event.create('acyan')
        .material('stone')
       .hardness(0.5)

  event.create('agreen')
        .material('stone')
       .hardness(0.5)
     
  event.create('apurple')
        .material('stone')
       .hardness(0.5)
     
  event.create('ared')
        .material('stone')
       .hardness(0.5)

   event.create('ayellow')
        .material('stone')
       .hardness(0.5)
  
   event.create('betrayed1')
       .material('stone')
      .hardness(0.5)

   event.create('betrayed2')
       .material('stone')
      .hardness(0.5)

   event.create('betrayed3')
       .material('stone')
      .hardness(0.5)

   event.create('betrayed4')
       .material('stone')
      .hardness(0.5)

   event.create('betrayed5')
       .material('stone')
      .hardness(0.5)

   event.create('betrayed6')
       .material('stone')
      .hardness(0.5)

   event.create('betrayed7')
       .material('stone')
      .hardness(0.5)

   event.create('betrayed8')
       .material('stone')
      .hardness(0.5)

   event.create('betrayed9')
       .material('stone')
      .hardness(0.5)

   event.create('betrayed10')
       .material('stone')
      .hardness(0.5)

   event.create('betrayed11')
       .material('stone')
      .hardness(0.5)

   event.create('betrayed12')
       .material('stone')
      .hardness(0.5)

   event.create('betrayed13')
       .material('stone')
      .hardness(0.5)

   event.create('betrayed14')
       .material('stone')
      .hardness(0.5)

   event.create('betrayed15')
       .material('stone')
      .hardness(0.5)

   event.create('betrayed16')
       .material('stone')
      .hardness(0.5)

   event.create('betrayed17')
       .material('stone')
      .hardness(0.5)

   event.create('betrayed18')
       .material('stone')
      .hardness(0.5)
      
   event.create('betrayed19')
       .material('stone')
      .hardness(0.5)
      
   event.create('betrayed20')
       .material('stone')
      .hardness(0.5)
      
   event.create('betrayed21')
       .material('stone')
      .hardness(0.5)
      
   event.create('betrayed22')
       .material('stone')
      .hardness(0.5)
      
   event.create('betrayed23')
       .material('stone')
      .hardness(0.5)
      
   event.create('betrayed24')
       .material('stone')
      .hardness(0.5)
      
   event.create('betrayed25')
       .material('stone')
      .hardness(0.5)
      
   event.create('betrayed26')
       .material('stone')
      .hardness(0.5)
      
   event.create('betrayed27')
       .material('stone')
      .hardness(0.5)
      
   event.create('betrayed28')
       .material('stone')
      .hardness(0.5)
      
   event.create('betrayed29')
       .material('stone')
      .hardness(0.5)
      
   event.create('betrayed30')
       .material('stone')
      .hardness(0.5)
      
   event.create('betrayed31')
       .material('stone')
      .hardness(0.5)
      
   event.create('betrayed32')
       .material('stone')
      .hardness(0.5)
      
   event.create('betrayed33')
       .material('stone')
      .hardness(0.5)
      
   event.create('betrayed34')
       .material('stone')
      .hardness(0.5)
            
   event.create('podzol1')
       .material('dirt')
      .hardness(0.5)
                  
   event.create('testmodel')
   .material('stone')
  .hardness(0.5)
 
  event.create('solidblack')
     .material('stone')
    .hardness(0.5)
 
    event.create('solidwhite')
     .material('stone')
    .hardness(0.5)
})

onEvent('fluid.registry', event => {
    // These first examples are 1.16.5 and 1.18.2 syntax
    
    // Basic "thick" (looks like lava) fluid with red tint
    event.create('chemical_waste_lime')
      .thickTexture(0x00ff9e)
      .bucketColor(0x00ff9e)
      .displayName('Teal Chemical Waste')
                 
    // Basic "thin" (looks like water) fluid with cyan tint, has no bucket and is not placeable
    event.create('thick_fluid')
      .thinTexture(0xFF0000)
      .bucketColor(0x00FFFF)
      .displayName('Thin Fluid') // both these methods are 1.18.2+ only
        .noBlock() 
    
    // Fluid with custom textures
    event.create('strawberry_cream')
        .displayName('Strawberry Cream')
      .stillTexture('kubejs:block/strawberry_still')
      .flowingTexture('kubejs:block/strawberry_flow')
      .bucketColor(0xFF33FF)
    
    // For 1.18.1 the syntax is slightly different
    event.create('thick_fluid', fluid => {
         fluid.textureThick(0xFF0000) // the texture method names are different in 1.18.1 and below, textureXyz instead of xyzTexture
         fluid.bucketColor(0xFF0000)
         fluid.displayName('Thick Fluid')
    })
  })