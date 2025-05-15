from remake1.constant.enums import Direction
import random


class Strategy:
    def __init__(self):
        pass

    # 简单AI - 随机移动
    @classmethod
    def simple_ai(cls, ball_state, paddle_state):
        if random.random() < 0.5:  # 50%的几率改变方向
            return Direction.UP if random.random() < 0.5 else Direction.DOWN
        return Direction.IDLE

    @classmethod
    # 中等AI - 跟随球移动，但有延迟和误差
    def medium_ai(cls, ball_state, paddle_state, paddle_height):
        # 只关心球的y坐标
        paddle_center = paddle_state['y'] + paddle_height // 2
        ball_center = ball_state['y'] + paddle_height // 2

        # 添加一些随机误差
        error = random.randint(-10, 10)

        if abs(paddle_center - ball_center + error) > 30:  # 误差阈值
            return Direction.UP if paddle_center > ball_center + error else Direction.DOWN
        return Direction.IDLE

    @classmethod
    # 高级AI - 预测球的位置并拦截
    def advanced_ai(cls, ball_state, paddle_state, game_width, paddle_height):
        paddle_center = paddle_state['y'] + paddle_height // 2
        ball_center = ball_state['y'] + paddle_height // 2

        # 预测球的轨迹
        if ball_state['speedx'] != 0:
            # 计算球到达挡板位置的时间
            distance_to_paddle = abs(ball_state['x'] - paddle_state['x'])
            time_to_paddle = distance_to_paddle / abs(ball_state['speedx'])

            # 预测球的y位置
            predicted_y = ball_center + ball_state['speedy'] * time_to_paddle

            # 确保预测位置在屏幕内
            predicted_y = max(0, min(predicted_y, game_width))

            # 移动到预测位置
            if abs(paddle_center - predicted_y) > 10:  # 小阈值确保精确
                return Direction.UP if paddle_center > predicted_y else Direction.DOWN

        return Direction.IDLE

    @classmethod
    # 专家AI - 高级预测+策略性失误
    def expert_ai(cls, ball_state, paddle_state, game_width,paddle_height,difficulty=0.9):
        paddle_center = paddle_state['y'] + paddle_height//2
        ball_center = ball_state['y'] + paddle_height // 2

        # 预测球的轨迹
        if ball_state['speedx'] != 0:
            distance_to_paddle = abs(ball_state['x'] - paddle_state['x'])
            time_to_paddle = distance_to_paddle / abs(ball_state['speedx'])
            predicted_y = ball_center + ball_state['speedy'] * time_to_paddle
            predicted_y = max(0, min(predicted_y, game_width))

            # 有时故意不完美拦截 (根据难度级别)
            if random.random() > difficulty:
                predicted_y += random.randint(-50, 50)
                predicted_y = max(0, min(predicted_y, game_width))

            # 平滑移动
            move_threshold = 5  # 更精确的移动
            if abs(paddle_center - predicted_y) > move_threshold:
                return Direction.UP if paddle_center > predicted_y else Direction.DOWN

        return Direction.IDLE

    @classmethod
    # 反应式AI - 只在球靠近时移动
    def reactive_ai(cls, ball_state, paddle_state,paddle_height,reaction_distance=200):
        # 只当球靠近时才反应
        if abs(ball_state['x'] - paddle_state['x']) > reaction_distance:
            return Direction.IDLE

        paddle_center = paddle_state['y'] + paddle_height//2
        ball_center = ball_state['y'] + paddle_height // 2

        if abs(paddle_center - ball_center) > 20:
            return Direction.UP if paddle_center > ball_center else Direction.DOWN
        return Direction.IDLE
