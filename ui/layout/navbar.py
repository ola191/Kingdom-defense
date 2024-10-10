def layout_navbar(elements, available_width, available_height, spacing, side="right", top_margin=10, side_margin=10):
    """
    Arrange elements in a horizontal row (navbar) at the top of the screen.

    :param elements: List of elements (e.g., buttons) to be arranged.
    :param available_width: Width of the available area for layout.
    :param available_height: Height of the available area for layout.
    :param spacing: Space between elements.
    :param side: 'left' or 'right', to specify which side to align the elements.
    :param top_margin: Space from the top of the screen.
    :param side_margin: Space from the sides of the screen.
    :return: List of tuples with positions (x, y) for each element.
    """
    positions = []
    total_width = sum(element.get_size()[0] for element in elements) + (spacing * (len(elements) - 1))

    start_y = top_margin

    if side == "left":
        start_x = side_margin
        for element in elements:
            positions.append((start_x, start_y))

            element.position = (start_x, start_y)
            element.rect.topleft = element.position
            element.rect.size = element.get_size()

            start_x += element.get_size()[0] + spacing

    elif side == "right":
        start_x = available_width - total_width - side_margin
        for element in elements:
            positions.append((start_x, start_y))

            element.position = (start_x, start_y)
            element.rect.topleft = element.position
            element.rect.size = element.get_size()

            start_x += element.get_size()[0] + spacing

    return positions