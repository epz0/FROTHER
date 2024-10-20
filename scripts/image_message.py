

def create_multi_image_content_block(imgprompt, list_images64, list_ids, detail='auto'):
    """Function to create multi image content blocks.

    Args:
        imgprompt (str): Prompt to analyse the images.
        list_images64 (list): List of the base64 images.
        list_ids (list): list of the ids.
        detail (str): high or low, for the level fidelity. Auto is default.

    Returns:
        ls_content: list of the content block withe multi images setup.
    """
    ls_content = []

    ls_content.append({
        "type": "text",
        "text": imgprompt,
    })

    for i in range(len(list_ids)):
        ls_content.append({
            'type':'image_url',
            'image_url':{
                'url': f"data:image/jpeg;base64,{list_images64[i]}",
                'detail':detail
            }
        })

    return ls_content

def create_id_content_block(ids_prompt, ids_list):
    ls_content_id =[]

    ids_list = ','.join(ids_list)

    ls_content_id.append({
        "type": "text",
        "text": ids_prompt,
    })

    ls_content_id.append({
        "type": "text",
        "text": ids_list,
    })
    return ls_content_id
