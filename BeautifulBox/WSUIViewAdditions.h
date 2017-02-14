//
//  WSUIViewAdditions.h
//  WiseSeller
//
//  Created by steven on 14-5-4.
//  Copyright (c) 2014年 steven. All rights reserved.
//

#import <Foundation/Foundation.h>
#import <UIKit/UIKit.h>
/**
 *	@brief	UIView 拓展.
 */
@interface UIView (WSLibrary){
    
}
/**
 *	@brief	frame.origin.x简写.
 */
@property (nonatomic) CGFloat left;

/**
 *	@brief	frame.origin.y简写.
 */
@property (nonatomic) CGFloat top;

/**
 *	@brief	frame.origin.x + frame.size.width简写.
 *  赋值后, frame.origin.x = right - frame.size.width.
 */
@property (nonatomic) CGFloat right;

/**
 *	@brief	frame.origin.y + frame.size.height简写.
 赋值后, frame.origin.y = bottom - frame.size.height.
 */
@property (nonatomic) CGFloat bottom;

/**
 *	@brief	frame.size.width简写.
 *  赋值后, frame.size.width = width.
 */
@property (nonatomic) CGFloat width;

/**
 *	@brief	frame.size.height简写.
 *  赋值后, frame.size.height = height.
 */
@property (nonatomic) CGFloat height;

/**
 *	@brief	center.x简写.
 *  赋值后,center.x = centerX.
 */
@property (nonatomic) CGFloat centerX;

/**
 *	@brief	center.y简写.
 *  赋值后, center.y = centerY.
 */
@property (nonatomic) CGFloat centerY;

/**
 *	@brief  frame.origin简写.
 *  赋值后, frame.origin = origin.
 */
@property (nonatomic) CGPoint origin;

/**
 *	@brief	frame.size简写.
 *  赋值后, frame.size = size.
 */
@property (nonatomic) CGSize size;

/**
 *	@brief	屏幕上的x坐标.
 */
@property (nonatomic, readonly) CGFloat screenX;

/**
 *	@brief	屏幕上的y坐标.
 */
@property (nonatomic, readonly) CGFloat screenY;

/**
 *	@brief	移除实例View所有子视图.
 */
- (void)removeAllSubviews;

/**
 *	@brief	递归获取aView所有子视图.
 *
 *	@param 	aView 	源视图.
 *
 *	@return	子视图数组集合.
 */
- (NSArray *)allSubviews:(UIView *)aView;

/**
 *	@brief	实例View到父Window的视图路径.
 *
 *	@return	父View路径集合.
 */
- (NSArray *)viewPath;

/**
 *	@brief	显示aView视图目录结构日志,主要用于日志打印.
 *
 *	@param 	aView 	原始图.
 *
 *	@return	日志字符串,可直接输出.
 */
- (NSString *)displayViews:(UIView *)aView;
@end
