# Syne 
#### Project developed at Hack CMU 2018

**Video:** https://www.youtube.com/watch?v=YZfCtv7U_dM&t=2s

Over 70 million people globally are mute, and many more with other hearing or speech impairments. Their communication is limited to sign language, and without a translator, conveying information to society at large is nearly impossible. However, especially in developing countries, many facilities still lack the resources to communicate with mute people. Participating in class, asking for help, and other day to day tasks most of us take for granted are challenges for those with such speech disabilities. Introducing, Syne! Syne is a tensorflow-based sign language processing system that allows mute people to efficiently communicate with the outside world. 

This system gathers (x, y, z) coordinates of each of the 15 joints in our hands using a leap motion sensor, which we then map to 3D vectors relative to the position of our palm. These vectors were normalized in order to ensure that the size of the hand doesn’t affect the accuracy of the system. Our neural network takes in the 45 data points, and, using three dense hidden layers, categorizes the hand gesture as one of the 26 letters. This model was trained with thousands of readings for each letter, and while training, received a validation accuracy of over 99%.

This system could be set up at any facilities, not only allowing people to communicate more easily in their day to day lives, but also opening up a plethora of employment and other opportunities. We believe in empowering those with disabilities to carry out day to day tasks independently and seamlessly. With Syne, we eliminate the need to rely on translators, and open up a world of possibilities.
