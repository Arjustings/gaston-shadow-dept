/* Gaston Grandiose's Shadow Dept. — the ten scenes.
   P(file, x, y, rollDegrees, k?) : where each prop sits in the solved shadow (k = extra size multiplier).
   scale  = size of every prop in the scene, so they stay true to each other.
   decor  = artwork printed on the paper screen (see DECOR in index.html). sea:true hides the bottom strip behind waves.
   quotes = Madame Aigre's reviews for this scene: [dreadful, doubtful, good, perfect]. */
const P = (id, x, y, roll = 0, k = 1, yaw = 0) => ({ id, k, sol: { x, y, roll: roll * Math.PI / 180, yaw } });
export const LEVELS = [
  { name: 'Le Lapin', beast: 'the rabbit', ask: 'A rabbit!', guide: 'paper', scale: 1, decor: 'meadow',
    line: 'A gentle start. I have a watermelon and a pair of ballet slippers.', line2: 'Give me ears the back row can count.',
    props: [P('melon', 0, 3.6), P('slipper', -.8, 5.85, 12), P('slipper', .8, 5.85, -12)],
    quotes: [
      ['“I counted no ears. I counted one melon.”', '“A fruit stall fell over. I did not applaud.”', '“The rabbit, I am told, was in there somewhere.”', '“Two slippers and a melon met a lamp. That is the whole review.”'],
      ['“A rabbit, possibly. Or a melon with ambitions.”', '“One ear pointed at heaven, the other at the exit.”', '“It twitched. I am told that was the stagehand.”', '“Rabbit-adjacent. I have seen better in a hat.”'],
      ['“Ears! Two of them! Roughly where ears go!”', '“I very nearly offered it a carrot.”', '“For a moment I forgot those ears had danced Swan Lake.”', '“A fine rabbit. A little lopsided, like all the best ones.”'],
      ['“I shall never eat watermelon again. It looked at me.”', '“So real that row two hid their lettuce.”', '“Perfect ears. I checked them against my own.”', '“Somewhere a magician is weeping into his hat.”']] },
  { name: 'La Tour Eiffel', beast: 'the tower', ask: 'The Eiffel Tower!', scale: .62, decor: 'paris',
    line: 'Paris, in one evening! I have a stepladder, a wine bottle, a hatpin and a bow tie.', line2: 'Make it tall. Make them homesick.',
    props: [P('stepladder', 0, 3.53), P('winebottle', 0, 5.6), P('hatpin', 0, 7.0, 180), P('bowtie', 0, 4.9)],
    quotes: [
      ['“I have seen the Eiffel Tower. That was a stepladder having a bad day.”', '“Paris deserves an apology. So does the ladder.”', '“A bottle, a ladder, a tragedy.”', '“Monsieur Eiffel is spinning, and not gracefully.”'],
      ['“A tower of some sort. Pisa, perhaps.”', '“It leaned. I leaned with it. We both regret it.”', '“Tall, yes. Eiffel, no.”', '“The top wandered off without the bottom.”'],
      ['“Paris! Slightly crooked, but Paris!”', '“I felt homesick, and I live four streets away.”', '“A handsome tower. The bow tie was a daring touch.”', '“It stood. In this theatre, that is an achievement.”'],
      ['“I reached for my ticket to the top.”', '“So like the real thing that a pigeon landed on it.”', '“Three hundred metres of iron from one stepladder. Witchcraft.”', '“I wept. I am from Lyon and I still wept.”']] },
  { name: 'Le Monstre Marin', beast: 'the sea monster', ask: 'A sea monster!', sea: true, decor: 'sea', scale: 1,
    line: 'The house is full and I have a teapot, a baguette, a fan and a fork.', line2: 'When the lamp comes on, they must scream.',
    props: [{ id: 'teapot', file: 'teapot-v1', k: .85, sol: { x: 1.2, y: 6.0, roll: .15, yaw: 0 } }, { id: 'baguette', k: 1.05, sol: { x: -.7, y: 3.5, roll: -.38, yaw: 0 } },
            { id: 'fan', k: .8, sol: { x: -1.35, y: 5.7, roll: 1.3, yaw: 0 } }, { id: 'fork', k: .7, sol: { x: 3.75, y: 6.95, roll: -1.2, yaw: 0 } }],
    quotes: [
      ['“I saw a tea service. So did my mother.”', '“The monster appeared to be lunch.”', '“A baguette went for a swim. Nobody screamed.”', '“My bathwater has more menace.”'],
      ['“Something stirred in the waves. Possibly indigestion.”', '“A fine silhouette, if you have never seen a sea.”', '“The beast had ambition. It lacked a neck.”', '“I squinted. It squinted back. Neither of us was convinced.”'],
      ['“The serpent rose. Row three ducked.”', '“For a moment, reader, I forgot the baguette.”', '“The fork was a tongue. I am almost certain of it.”', '“Very nearly terrifying. A firm ‘oh my’.”'],
      ['“I have cancelled my holiday by the coast.”', '“A teapot? Never. I saw the beast of the deep.”', '“Row one is still under their seats.”', '“It looked at me. I have not slept.”']] },
  { name: 'Pinocchio', beast: 'the puppet', ask: 'Pinocchio!', scale: 1.05, decor: 'strings',
    line: 'A wooden boy with a famous nose. I have a ball of wool, a funnel, a paintbrush, a quill and a ruff.', line2: 'The longer the nose, the louder the gasp.',
    props: [P('yarnball', -.35, 4.45), P('funnel', -.47, 6.36, 10), P('paintbrush', 1.87, 4.55, -80), P('quill', -1.4, 6.55, 30), P('ruff', -.35, 2.8)],
    quotes: [
      ['“A ball of wool sat there. It did not lie, and it did not live.”', '“No nose. No boy. No refund, apparently.”', '“I have seen more character in a sock drawer.”', '“Geppetto would have taken up plumbing.”'],
      ['“A puppet of some kind, or a hat with a problem.”', '“The nose was there. The rest was a rumour.”', '“It wobbled like a boy who has not done his homework.”', '“Nearly a nose. Nearly a boy. Nearly my bedtime.”'],
      ['“The nose! It grew as I watched! Or I leaned in.”', '“A proper wooden boy, strings not included.”', '“I believed him, which is unwise with this one.”', '“Charming. I should not trust him with my purse.”'],
      ['“He lied to me from across the room and I thanked him.”', '“That nose could hang a week’s washing.”', '“A real boy at last. Someone tell the fairy.”', '“I looked for the strings. There were none. I am unwell.”']] },
  { name: 'La Montgolfière', beast: 'the balloon', ask: 'A hot-air balloon!', scale: .8, decor: 'clouds',
    line: 'Up, over the rooftops! I have a paper lantern, a picnic basket, two drumsticks and a pennant.', line2: 'If it does not float, neither does my reputation.',
    props: [P('lantern', 0, 5.6), P('basket', 0, 2.8), P('drumstick', -.65, 3.95, 15), P('drumstick', .65, 3.95, -15), P('pennant', .5, 7.4)],
    quotes: [
      ['“It did not float. It did not try.”', '“A lantern and a basket, not on speaking terms.”', '“I have seen picnics with more lift.”', '“The balloon went down. So did the evening.”'],
      ['“It hovered, in the way a brick hovers.”', '“The basket seemed to be leaving without the balloon.”', '“Aloft, if one is generous. I am not.”', '“A balloon, or a very large onion.”'],
      ['“Up it went! I waved. I am not proud of it.”', '“I nearly asked for a seat in the basket.”', '“A handsome balloon, a touch tipsy on its ropes.”', '“The ropes held. So did my attention, which is rarer.”'],
      ['“I felt the floor leave. It was only my chair, but still.”', '“So real I checked my hat for wind.”', '“Row four threw ballast.”', '“I have booked passage to the moon.”']] },
  { name: 'Le Voilier', beast: 'the ship', ask: 'A sailing ship!', sea: true, decor: 'ocean', scale: .95,
    line: 'To sea! I have a violin, a broom, a pair of bloomers, a coat hanger, a sock and a corkscrew.', line2: 'Hoist whatever you find.',
    props: [P('violin', -1.25, 4.02, 68), P('hanger', .01, 4.86, -90), P('broom', 1.54, 5.61, 180), P('corkscrew', 1.54, 5.61, 180), P('bloomers', 1.25, 3.26, -95), P('sock', 2.8, 4.14, 111)],
    quotes: [
      ['“It sank before it sailed.”', '“A violin drowned tonight. Say a prayer.”', '“Laundry day, not a regatta.”', '“The only thing launched was my patience.”'],
      ['“A vessel, loosely. A raft, strictly.”', '“The sail and the mast are no longer friends.”', '“She listed. So did the audience.”', '“Seaworthy as a sieve, but shaped like a boat.”'],
      ['“A ship! With bloomers for a sail, as God intended.”', '“I smelled salt. It may have been the pretzels.”', '“She sailed handsomely, underwear and all.”', '“Fit for the open sea, or at least the canal.”'],
      ['“I was seasick in the best possible way.”', '“The bloomers filled with wind and so did my heart.”', '“Admiral Nelson would have saluted the sock.”', '“I waved a handkerchief from the quay of my seat.”']] },
  { name: "L'Éléphant", beast: 'the elephant', ask: 'An elephant!', scale: 1.05, decor: 'ring',
    line: 'The real one is on strike. I have a bass drum, a trumpet, a tambourine and four odd things for legs.', line2: 'Four legs, please. Any four.',
    props: [P('bassdrum', -.5, 5.1), P('tambourine', 1.5, 5.7), P('trumpet', 2.3, 4.55, -90), P('jugglingclub', .55, 3.25), P('peppermill', 1.1, 2.95), P('boot', -1.55, 3.05), P('milkbottle', -.85, 2.9)],
    quotes: [
      ['“A drum, a trumpet, and no elephant in the room.”', '“The real elephant was right to strike.”', '“Four legs were promised. I counted a kitchen.”', '“A brass band fell down the stairs.”'],
      ['“Large and grey in spirit only.”', '“The trunk was pointing at something else entirely.”', '“An elephant as described by someone who has not met one.”', '“It had the weight. It lacked the animal.”'],
      ['“A trunk! Ears! A leg made of pepper!”', '“Majestic, if a little percussive.”', '“I very nearly threw it a peanut.”', '“A fine beast. One leg was a boot, and I respect that.”'],
      ['“It trumpeted. I know it was a trumpet. I still jumped.”', '“Row one fed it. Nobody stopped them.”', '“An elephant never forgets, and nor shall I.”', '“I felt the floor shake. The drum has an alibi.”']] },
  { name: 'Le Moulin', beast: 'the windmill', ask: 'A windmill!', scale: .8, decor: 'hills',
    line: 'The Moulin itself! I have a milk churn, a colander, an alarm clock, a glove and four things that will pass for sails.', line2: 'Four sails. They need not match.',
    props: [P('milkchurn', 0, 3.42), P('colander', 0, 5.04, 180), P('alarmclock', 0, 5.2), P('tennisracket', 1.04, 6.25, -45), P('carpetbeater', -1.09, 6.3, 45), P('flyswatter', .95, 4.25, -135), P('butterflynet', -1.09, 4.1, 135), P('glove', 0, 6.1)],
    quotes: [
      ['“It did not turn. It did not mill. It did not anything.”', '“A milk churn in a hat.”', '“Four sails, pointing five ways.”', '“Don Quixote would have ridden straight past.”'],
      ['“A mill after a strong wind and a stronger drink.”', '“The sails seemed to be leaving separately.”', '“Round, tall and confused, like my late husband.”', '“Windmill-ish. Wind not included.”'],
      ['“Four sails, none of them matching, all of them proud.”', '“I swear the racket moved.”', '“A proper Moulin. One almost expects a cancan.”', '“Handsome! The butterfly net was inspired.”'],
      ['“I felt a breeze. Row two lost a hat.”', '“So fine a mill I ordered flour.”', '“The Moulin Rouge is consulting its lawyers.”', '“Montmartre has a rival, made of sports equipment.”']] },
  { name: 'Le Dragon', beast: 'the dragon', ask: 'A dragon!', scale: .85, decor: 'crags',
    line: 'They want fire. I have an accordion, garden shears, a hose, a feather duster and half a garden shed.', line2: 'Do not ask where the croissant goes.',
    props: [P('accordion', -.8, 3.9), P('hose', 1.2, 4.85, 35), P('shears', 3.3, 5.9, 10), P('croissant', 2.7, 6.5, 200), P('featherduster', 4.45, 6.0, -90), P('umbrella', -.6, 5.7, 15), P('kite', -1.65, 5.65, 35), P('saw', -3.0, 3.9, 180), P('rake', -.2, 3.2, 180), P('handfork', -1.3, 2.75, 180)],
    quotes: [
      ['“No fire. No wings. A garden shed in a heap.”', '“The dragon was slain by its own props.”', '“I have been more frightened by an accordion alone.”', '“Saint George stayed home.”'],
      ['“A lizard at best. A long lizard.”', '“It breathed dust, not fire.”', '“The wings went one way and the beast the other.”', '“A dragon drawn from memory by a man who once saw a goose.”'],
      ['“Fire! Or feathers! I ducked either way.”', '“Proper wings, proper teeth, proper nonsense.”', '“It snapped its shears at me and I rather liked it.”', '“A dragon with a croissant for horns. Only in Paris.”'],
      ['“My programme is singed.”', '“Row one is asking for a knight.”', '“I counted the teeth. Then I stopped counting and left.”', '“It breathed feather duster and I felt the heat.”']] },
  { name: 'Gaston le Grand', beast: 'the ringmaster', ask: 'Me!', scale: .85, decor: 'spot',
    line: 'The finale is the finest subject in Paris: myself. I have a top hat, a globe, a barrel and everything left in the wagon.', line2: 'Flatter me.',
    props: [P('barrel', 0, 4.15), P('globe', 0, 5.65), P('tophat', 0, 7.05), P('handlebars', 0, 5.2), P('megaphone', 1.3, 5.2, 15), P('scrubbrush', -1.25, 5.0), P('lightbulb', -2.25, 5.1, 90), P('cane', -2.8, 4.6, 8), P('rollingpin', -.42, 2.9), P('bowlingpin', .42, 2.95, 180)],
    quotes: [
      ['“That is not Gaston. Gaston has a shape.”', '“He will sue. I will testify.”', '“A barrel fell on a hat shop.”', '“I have seen the man. He is rounder and louder.”'],
      ['“A gentleman of some description. Not this one.”', '“The moustache was there. The dignity was not.”', '“Like Gaston after a long tour and a short dinner.”', '“A ringmaster, roughly, if one squints with both eyes.”'],
      ['“The belly! The hat! The unearned confidence!”', '“Uncanny. I expected it to overcharge me.”', '“A fine likeness. He has never looked so quiet.”', '“The moustache alone deserved its own bow.”'],
      ['“I could not tell which was the man and which the barrel.”', '“He bowed to himself. It was the proudest I have seen him.”', '“The shadow asked for a raise.”', '“Magnifique. Even the megaphone seemed pleased.”']] },
];
