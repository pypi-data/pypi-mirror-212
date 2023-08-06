#pragma once

#include <regex>

#include "common/vector/value_vector.h"

namespace kuzu {
namespace function {
namespace operation {

struct BaseRegexpOperation {
    static inline std::string parseCypherPatten(const std::string& pattern) {
        // Cypher parses escape characters with 2 backslash eg. for expressing '.' requires '\\.'
        // Since Regular Expression requires only 1 backslash '\.' we need to replace double slash
        // with single
        return std::regex_replace(pattern, std::regex(R"(\\\\)"), "\\");
    }

    static inline void copyToKuzuString(
        const std::string& value, common::ku_string_t& kuString, common::ValueVector& valueVector) {
        if (!common::ku_string_t::isShortString(value.length())) {
            kuString.overflowPtr = reinterpret_cast<uint64_t>(
                common::StringVector::getInMemOverflowBuffer(&valueVector)
                    ->allocateSpace(value.length()));
        }
        kuString.set(value);
    }
};

} // namespace operation
} // namespace function
} // namespace kuzu
