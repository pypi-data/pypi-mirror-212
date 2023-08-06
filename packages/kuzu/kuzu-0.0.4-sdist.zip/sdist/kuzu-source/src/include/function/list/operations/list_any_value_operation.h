#pragma once

#include "common/vector/value_vector_utils.h"

namespace kuzu {
namespace function {
namespace operation {

struct ListAnyValue {
    template<typename T>
    static inline void operation(common::list_entry_t& input, T& result,
        common::ValueVector& inputVector, common::ValueVector& resultVector) {
        auto inputValues = common::ListVector::getListValues(&inputVector, input);
        auto inputDataVector = common::ListVector::getDataVector(&inputVector);
        auto numBytesPerValue = inputDataVector->getNumBytesPerValue();

        for (auto i = 0; i < input.size; i++) {
            if (!(inputDataVector->isNull(input.offset + i))) {
                common::ValueVectorUtils::copyValue(
                    (uint8_t*)(&result), resultVector, inputValues, *inputDataVector);
                break;
            }
            inputValues += numBytesPerValue;
        }
    }
};

} // namespace operation
} // namespace function
} // namespace kuzu
