#include "executor/robot_executor.h"

namespace executor {

Executor::Executor()
    : m_x(DEFAULT_COORDINATE)
    , m_y(DEFAULT_COORDINATE)
    , m_heading(DEFAULT_HEADING)
    , m_initialized(false) {
}

Heading Executor::normalizeHeading(int32_t h) {
    int32_t n = h % HEADING_MODULO;
    if (n < 0) {
        n += HEADING_MODULO;
    }
    return static_cast<Heading>(n);
}

void Executor::init(int32_t x, int32_t y, Heading heading) {
    std::lock_guard<std::mutex> lock(m_mutex);
    m_x = x;
    m_y = y;
    m_heading = normalizeHeading(static_cast<int32_t>(heading));
    m_initialized = true;
}

void Executor::turnRight() {
    std::lock_guard<std::mutex> lock(m_mutex);
    if (!m_initialized) {
        return;
    }
    m_heading = static_cast<Heading>(
        (static_cast<int32_t>(m_heading) + HEADING_RIGHT_DELTA) % HEADING_MODULO);
}

void Executor::turnLeft() {
    std::lock_guard<std::mutex> lock(m_mutex);
    if (!m_initialized) {
        return;
    }
    m_heading = static_cast<Heading>(
        (static_cast<int32_t>(m_heading) + HEADING_LEFT_DELTA) % HEADING_MODULO);
}

void Executor::getStatus(int32_t& x, int32_t& y, Heading& heading) const {
    std::lock_guard<std::mutex> lock(m_mutex);
    if (!m_initialized) {
        x = DEFAULT_COORDINATE;
        y = DEFAULT_COORDINATE;
        heading = DEFAULT_HEADING;
        return;
    }
    x = m_x;
    y = m_y;
    heading = m_heading;
}

} // namespace executor

