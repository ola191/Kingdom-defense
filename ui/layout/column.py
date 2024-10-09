def layout_column(elements, available_width, available_height, spacing):
    """
    Arrange elements in a column based on their sizes.

    :param elements: List of elements (e.g., buttons) to be arranged.
    :param available_width: Width of the available area for layout.
    :param available_height: Height of the available area for layout.
    :param spacing: Space between elements.
    :return: List of tuples with positions (x, y) for each element.
    """

    positions = []
    total_height = sum(element.get_size()[1] for element in elements) + (spacing * (len(elements) - 1))

    # Calculate starting Y position to center the column vertically
    start_y = (available_height - total_height) // 2

    for element in elements:
        # Center each button within the available width
        x = (available_width - element.get_size()[0]) // 2
        positions.append((x, start_y))

        element.position = (x, start_y)
        #Updating rect of the button class
        element.rect.topleft = element.position
        element.rect.size = element.get_size()

        start_y += element.get_size()[1] + spacing

    return positions