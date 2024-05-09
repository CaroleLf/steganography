import numpy as np
import matplotlib.image as mpimg
import sys
from PIL import Image

def start():
    """
    This function recup the parameter to know the mode( decode or encode), the path of the img to encode/decode
    and the path of the file that contains the message
    """
    # Checking if there are the minimal two parameters set
    if len(sys.argv) > 2:
        # get the mode
        mode = sys.argv[1]
        # get the path of the img to encode/decode
        path_img = sys.argv[2]
        img = get_image(path_img)
        if mode == "encode":
            # get the path of file that contains the message
            path_message = sys.argv[3]
            encode(img, path_message)
        elif mode == "decode":
            message = decode(img)
            print("Message décodé : ", message)
        else:
            raise ValueError("Entrer un mode valide (encode/decode)")
    else:
        raise ValueError("Le nombre de paramètre n'est pas valide,"
                         " il faut au moins 2 parametres python3 steganographie.py <mode> <chemin image>")


def decode(image):
    """
    This function decodes the image and returns the message hide in the image
    Args:
        image: ndarray representing the image
    Returns:
        message hidden in the image
    """
    binary_message = []
    image_int = (image * 255).astype(np.uint8)
    for value in image_int:
        for pixel in value:
            r, g, b, _ = messageToBinary(pixel)
            # Take the LSB of the red
            binary_message += r[-1]
            # Take the LSB of the green
            binary_message += g[-1]
            # Take the LSB of the blue
            binary_message += b[-1]
    all_bytes = [binary_message[i: i + 8] for i in range(0, len(binary_message), 8)]
    binary_message = ''.join([''.join(bits) for bits in all_bytes])
    decoded_message = ''
    for i in range(0, len(binary_message), 8):
        byte = binary_message[i:i + 8]
        decoded_message += chr(int(byte, 2))
        if decoded_message[-5:] == "#####":
            break
    return decoded_message[:-5]


def encode(image, path_message: str):
    """
    Function that encode a message into the image provide, the ouput is saved as output.png
    Args:
        image: image where message will be hidden
        path_message: path of the file where the message will be hidden

    """
    message = get_file_content(path_message)
    imgEncoded = hideMessage(image, message)
    image = Image.fromarray(imgEncoded)
    image.save('output.png')


def hideMessage(image, message: str):
    """
    Function that hides a message into the image
    Args:
        image: image where message will be hidden
        message: message to be hidden, type : str

    Returns:

    """
    # Get the size of the img
    numberBytesImg = image.shape[0] * image.shape[1]
    if len(message) > numberBytesImg:
        raise ValueError("Le message est trop long par rapport à l'image fourni, opération impossible")
    #Delimitation of our message
    message += "#####"
    messageBinary = messageToBinary(message)
    # len of the secret
    secretLen = len(messageBinary)
    # counter of hidden bit
    dataLen = 0
    for index_row, row in enumerate(image):
        for index_pixel, pixel in enumerate(row):
            # convert pixel to binary
            r, g, b, _ = messageToBinary(pixel)
            if dataLen < secretLen:
                # Modify the LSB of the red
                pixel[0] = int(r[:-1] + messageBinary[dataLen], 2)
                dataLen += 1
            if dataLen < secretLen:
                # Modify the LSB of the green
                pixel[1] = int(g[:-1] + messageBinary[dataLen], 2)
                dataLen += 1
            if dataLen < secretLen:
                # Modify the LSB of the blue
                pixel[2] = int(b[:-1] + messageBinary[dataLen], 2)
                dataLen += 1

            # Update the pixel in the image
            image[index_row, index_pixel, :3] = pixel[:3]
            # check if the number of bit hidden is equal or upper than the size of the secret
            if dataLen >= secretLen:
                break
        if dataLen >= secretLen:
            break
    return image


def messageToBinary(message: str):
    """
        Transform a  string to a binary depending on the type of message
    Args:
        message: message to transform, type str or ndarray

    Returns:
        Binary message
    """
    encode_message = None
    if type(message) == str:
        encode_message = ''.join(format(ord(i), '08b') for i in message)
    elif type(message) == np.ndarray:
        encode_message = [format(i, "08b") for i in message]
    return encode_message


def get_image(path: str):
    """
        From the given path return the image as a numpy array
    Args:
        path: path of the img, type : string

    Returns:
        image as a numpy array
    """
    image = mpimg.imread(path)
    writable_image = np.array(image)
    return writable_image


def get_file_content(path):
    """
        From path return the content
    Args:
        path: path of the file that contains the message, type : string
    Returns:
        contents of the file, type : string
    """
    with open(path) as f:
        contents = f.read()
    return contents


if __name__ == '__main__':
    start()
