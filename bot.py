import json
import os
import numpy as np
import tensorflow as tf
import model, sample, encoder

import discord
global previous_message
global botUser
botUser = None
previous_message = None
client = discord.Client()

@client.event
async def on_ready():
    global previous_message
    global botUser

    previous_message = None
    botUser = client.user
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    global previous_message
    print(previous_message)

    if message.author == client.user:
        return

    if message.content.startswith('!'):
        if len(message.content) >= 1900:
            message.content = message.content[-1900:]

        if message.content == '!':
            text = generate("")
        else:
            text = generate(message.content[1:])

        previous_message = await message.channel.send(message.content[1:] + text)
        for _ in range(10):
            text = generate(previous_message.content)
            await previous_message.edit(content=previous_message.content + text)

    if message.content == "m" and previous_message:
        n = 10
        await message.delete()
        async with message.channel.typing():
            for _ in range(n):
                text = generate(previous_message.content)
                if len(previous_message.content + text) >= 1800:
                    previous_message = await message.channel.send(text)
                else:
                    await previous_message.edit(content = previous_message.content + text)

def generate(
    input_text = ""
):
    context_tokens = enc.encode(input_text)
    generated = 0
    for _ in range(nsamples // batch_size):
        out = sess.run(output, feed_dict={
            context: [context_tokens for _ in range(batch_size)]
        })[:, len(context_tokens):]
        for i in range(batch_size):
            generated += 1
            text = enc.decode(out[i])
            return(text.split("<|endoftext|>")[0]);

seed=None
nsamples=1
batch_size=1
length=20
temperature=1
top_k=40
input_text=""
model_name='345M'
enc = encoder.get_encoder(model_name)
hparams = model.default_hparams()



with open(os.path.join('models', model_name, 'hparams.json')) as f:
    hparams.override_from_dict(json.load(f))
previousBotMessage = ""
if batch_size is None:
    batch_size = 1
assert nsamples % batch_size == 0
if length is None:
    length = hparams.n_ctx // 2
elif length > hparams.n_ctx:
    raise ValueError("Can't get samples longer than window size: %s" % hparams.n_ctx)
with tf.Session(graph=tf.Graph()) as sess:
    context = tf.placeholder(tf.int32, [batch_size, None])
    np.random.seed(seed)
    tf.set_random_seed(seed)
    output = sample.sample_sequence(
        hparams=hparams, length=length,
        context=context,
        batch_size=batch_size,
        temperature=temperature, top_k=top_k
    )
    saver = tf.train.Saver()
    ckpt = tf.train.latest_checkpoint(os.path.join('models', model_name))
    saver.restore(sess, ckpt)
    client.run('')